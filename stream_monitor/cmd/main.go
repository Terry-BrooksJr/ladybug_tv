package main

import (
	"context"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/ladybug-tv/stream-monitor/internal/monitor"
	"github.com/ladybug-tv/stream-monitor/internal/metrics"
	"github.com/ladybug-tv/stream-monitor/internal/health"
	"github.com/ladybug-tv/stream-monitor/pkg/config"
	
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	log "github.com/sirupsen/logrus"
)

func main() {
	// Parse command line flags
	configPath := flag.String("config", "config/monitor.yaml", "path to configuration file")
	flag.Parse()

	// Load configuration
	cfg, err := config.Load(*configPath)
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Setup logging
	setupLogging(cfg.Log.Level, cfg.Log.Format)

	log.Info("Starting Ladybug TV Stream Monitor")
	log.Infof("Version: %s", cfg.App.Version)

	// Initialize metrics
	metrics.Init()

	// Create stream monitor
	streamMonitor := monitor.New(cfg)

	// Setup HTTP routers
	mainRouter := setupMainRouter(streamMonitor)
	metricsRouter := setupMetricsRouter()

	// Start main HTTP server
	mainServer := &http.Server{
		Addr:         fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port),
		Handler:      mainRouter,
		ReadTimeout:  time.Duration(cfg.Server.ReadTimeout) * time.Second,
		WriteTimeout: time.Duration(cfg.Server.WriteTimeout) * time.Second,
	}

	// Start metrics HTTP server
	metricsServer := &http.Server{
		Addr:         fmt.Sprintf("%s:%d", cfg.Metrics.Host, cfg.Metrics.Port),
		Handler:      metricsRouter,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// Start servers in goroutines
	go func() {
		log.Infof("Starting main server on %s", mainServer.Addr)
		if err := mainServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Main server failed: %v", err)
		}
	}()

	go func() {
		log.Infof("Starting metrics server on %s", metricsServer.Addr)
		if err := metricsServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Metrics server failed: %v", err)
		}
	}()

	// Start stream monitoring
	go streamMonitor.Start()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info("Shutting down servers...")

	// Graceful shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	streamMonitor.Stop()

	if err := mainServer.Shutdown(ctx); err != nil {
		log.Errorf("Main server shutdown error: %v", err)
	}

	if err := metricsServer.Shutdown(ctx); err != nil {
		log.Errorf("Metrics server shutdown error: %v", err)
	}

	log.Info("Servers stopped")
}

func setupMainRouter(monitor *monitor.Monitor) *chi.Mux {
	r := chi.NewRouter()

	// Middleware
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(60 * time.Second))

	// Health check endpoints
	healthHandler := health.NewHandler()
	r.Get("/health", healthHandler.Health)
	r.Get("/ready", healthHandler.Ready)

	// Stream monitoring endpoints
	r.Route("/api/v1", func(r chi.Router) {
		r.Get("/streams", monitor.GetStreamsStatus)
		r.Get("/streams/{id}", monitor.GetStreamStatus)
		r.Post("/streams/{id}/check", monitor.CheckStream)
		r.Get("/stats", monitor.GetStats)
	})

	return r
}

func setupMetricsRouter() *chi.Mux {
	r := chi.NewRouter()
	r.Handle("/metrics", promhttp.Handler())
	return r
}

func setupLogging(level, format string) {
	// Set log level
	logLevel, err := log.ParseLevel(level)
	if err != nil {
		log.Warn("Invalid log level, using INFO")
		logLevel = log.InfoLevel
	}
	log.SetLevel(logLevel)

	// Set log format
	if format == "json" {
		log.SetFormatter(&log.JSONFormatter{})
	} else {
		log.SetFormatter(&log.TextFormatter{
			FullTimestamp: true,
		})
	}

	log.SetOutput(os.Stdout)
}
