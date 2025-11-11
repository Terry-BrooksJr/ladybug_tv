package main

import (
    "context"
    "fmt"
    "net/http"
    "os"
    "time"

    "github.com/go-redis/redis/v8"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    log "github.com/sirupsen/logrus"
)

var (
    ctx = context.Background()
    
    // Prometheus metrics
    streamHealthGauge = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "stream_health",
            Help: "Health status of streams (1 = healthy, 0 = unhealthy)",
        },
        []string{"channel_id"},
    )
    
    streamLatencyGauge = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "stream_latency_ms",
            Help: "Stream response latency in milliseconds",
        },
        []string{"channel_id"},
    )
    
    streamCheckCounter = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "stream_checks_total",
            Help: "Total number of stream health checks",
        },
        []string{"channel_id", "status"},
    )
)

type Config struct {
    RedisURL       string
    CheckInterval  time.Duration
    MetricsPort    string
    StreamBaseURL  string
}

type StreamMonitor struct {
    config      Config
    redisClient *redis.Client
}

func init() {
    // Register Prometheus metrics
    prometheus.MustRegister(streamHealthGauge)
    prometheus.MustRegister(streamLatencyGauge)
    prometheus.MustRegister(streamCheckCounter)
    
    // Configure logging
    log.SetFormatter(&log.JSONFormatter{})
    log.SetOutput(os.Stdout)
    log.SetLevel(log.InfoLevel)
}

func NewStreamMonitor(config Config) *StreamMonitor {
    opt, err := redis.ParseURL(config.RedisURL)
    if err != nil {
        log.Fatalf("Failed to parse Redis URL: %v", err)
    }
    
    rdb := redis.NewClient(opt)
    
    // Test Redis connection
    if err := rdb.Ping(ctx).Err(); err != nil {
        log.Fatalf("Failed to connect to Redis: %v", err)
    }
    
    log.Info("Connected to Redis successfully")
    
    return &StreamMonitor{
        config:      config,
        redisClient: rdb,
    }
}

func (sm *StreamMonitor) checkStreamHealth(channelID string, streamURL string) {
    start := time.Now()
    
    client := &http.Client{
        Timeout: 5 * time.Second,
    }
    
    resp, err := client.Head(streamURL)
    latency := time.Since(start).Milliseconds()
    
    if err != nil {
        log.WithFields(log.Fields{
            "channel_id": channelID,
            "error":      err.Error(),
        }).Warn("Stream health check failed")
        
        streamHealthGauge.WithLabelValues(channelID).Set(0)
        streamCheckCounter.WithLabelValues(channelID, "failed").Inc()
        
        // Store failure in Redis
        sm.redisClient.Set(ctx, fmt.Sprintf("stream:health:%s", channelID), "unhealthy", 5*time.Minute)
        return
    }
    defer resp.Body.Close()
    
    isHealthy := resp.StatusCode == http.StatusOK
    healthValue := 0.0
    status := "unhealthy"
    
    if isHealthy {
        healthValue = 1.0
        status = "healthy"
    }
    
    // Update metrics
    streamHealthGauge.WithLabelValues(channelID).Set(healthValue)
    streamLatencyGauge.WithLabelValues(channelID).Set(float64(latency))
    streamCheckCounter.WithLabelValues(channelID, status).Inc()
    
    // Store in Redis
    sm.redisClient.Set(ctx, fmt.Sprintf("stream:health:%s", channelID), status, 5*time.Minute)
    sm.redisClient.Set(ctx, fmt.Sprintf("stream:latency:%s", channelID), latency, 5*time.Minute)
    
    log.WithFields(log.Fields{
        "channel_id": channelID,
        "status":     status,
        "latency_ms": latency,
    }).Info("Stream health check completed")
}

func (sm *StreamMonitor) getActiveChannels() ([]string, error) {
    // Get list of active channels from Redis
    channels, err := sm.redisClient.SMembers(ctx, "active_channels").Result()
    if err != nil {
        return nil, err
    }
    return channels, nil
}

func (sm *StreamMonitor) monitorStreams() {
    ticker := time.NewTicker(sm.config.CheckInterval)
    defer ticker.Stop()
    
    log.Info("Starting stream monitoring")
    
    for {
        channels, err := sm.getActiveChannels()
        if err != nil {
            log.WithError(err).Error("Failed to get active channels")
            <-ticker.C
            continue
        }
        
        log.WithField("channel_count", len(channels)).Info("Checking stream health")
        
        // Check each channel concurrently
        for _, channelID := range channels {
            go func(chID string) {
                streamURL := fmt.Sprintf("%s/hls/%s/playlist.m3u8", sm.config.StreamBaseURL, chID)
                sm.checkStreamHealth(chID, streamURL)
            }(channelID)
        }
        
        <-ticker.C
    }
}

func (sm *StreamMonitor) startMetricsServer() {
    http.Handle("/metrics", promhttp.Handler())
    
    log.WithField("port", sm.config.MetricsPort).Info("Starting metrics server")
    
    if err := http.ListenAndServe(":"+sm.config.MetricsPort, nil); err != nil {
        log.Fatalf("Failed to start metrics server: %v", err)
    }
}

func getEnv(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

func main() {
    config := Config{
        RedisURL:       getEnv("REDIS_URL", "redis://localhost:6379"),
        CheckInterval:  30 * time.Second,
        MetricsPort:    getEnv("METRICS_PORT", "9091"),
        StreamBaseURL:  getEnv("STREAM_BASE_URL", "http://localhost:8002"),
    }
    
    monitor := NewStreamMonitor(config)
    
    // Start metrics server in background
    go monitor.startMetricsServer()
    
    // Start monitoring streams
    monitor.monitorStreams()
}
