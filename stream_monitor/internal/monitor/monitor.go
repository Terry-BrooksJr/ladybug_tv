package monitor

import (
	"context"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/ladybug-tv/stream-monitor/internal/metrics"
	"github.com/ladybug-tv/stream-monitor/pkg/config"
	"github.com/ladybug-tv/stream-monitor/pkg/types"
	log "github.com/sirupsen/logrus"
)

type Monitor struct {
	cfg       *config.Config
	streams   map[string]*types.Stream
	mu        sync.RWMutex
	ctx       context.Context
	cancel    context.CancelFunc
	wg        sync.WaitGroup
}

func New(cfg *config.Config) *Monitor {
	ctx, cancel := context.WithCancel(context.Background())
	
	return &Monitor{
		cfg:     cfg,
		streams: make(map[string]*types.Stream),
		ctx:     ctx,
		cancel:  cancel,
	}
}

func (m *Monitor) Start() {
	log.Info("Stream monitor started")
	
	ticker := time.NewTicker(time.Duration(m.cfg.Monitor.CheckInterval) * time.Second)
	defer ticker.Stop()

	// Initial check
	m.checkAllStreams()

	for {
		select {
		case <-ticker.C:
			m.checkAllStreams()
		case <-m.ctx.Done():
			log.Info("Stream monitor stopping...")
			return
		}
	}
}

func (m *Monitor) Stop() {
	log.Info("Stopping stream monitor")
	m.cancel()
	m.wg.Wait()
}

func (m *Monitor) checkAllStreams() {
	m.mu.RLock()
	streams := make([]*types.Stream, 0, len(m.streams))
	for _, stream := range m.streams {
		streams = append(streams, stream)
	}
	m.mu.RUnlock()

	for _, stream := range streams {
		m.wg.Add(1)
		go func(s *types.Stream) {
			defer m.wg.Done()
			m.checkStream(s)
		}(stream)
	}
}

func (m *Monitor) checkStream(stream *types.Stream) {
	start := time.Now()
	
	log.Debugf("Checking stream: %s (%s)", stream.ID, stream.URL)

	ctx, cancel := context.WithTimeout(m.ctx, time.Duration(m.cfg.Monitor.Timeout)*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, "GET", stream.URL, nil)
	if err != nil {
		m.updateStreamStatus(stream.ID, false, err.Error(), 0)
		metrics.StreamCheckFailed.WithLabelValues(stream.ID, "request_error").Inc()
		return
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		m.updateStreamStatus(stream.ID, false, err.Error(), 0)
		metrics.StreamCheckFailed.WithLabelValues(stream.ID, "connection_error").Inc()
		return
	}
	defer resp.Body.Close()

	responseTime := time.Since(start).Milliseconds()

	if resp.StatusCode == http.StatusOK {
		m.updateStreamStatus(stream.ID, true, "OK", responseTime)
		metrics.StreamCheckSuccess.WithLabelValues(stream.ID).Inc()
		metrics.StreamResponseTime.WithLabelValues(stream.ID).Observe(float64(responseTime))
	} else {
		msg := fmt.Sprintf("HTTP %d", resp.StatusCode)
		m.updateStreamStatus(stream.ID, false, msg, responseTime)
		metrics.StreamCheckFailed.WithLabelValues(stream.ID, fmt.Sprintf("http_%d", resp.StatusCode)).Inc()
	}
}

func (m *Monitor) updateStreamStatus(id string, healthy bool, message string, responseTime int64) {
	m.mu.Lock()
	defer m.mu.Unlock()

	stream, exists := m.streams[id]
	if !exists {
		return
	}

	stream.Healthy = healthy
	stream.LastCheck = time.Now()
	stream.LastMessage = message
	stream.ResponseTime = responseTime

	if healthy {
		stream.ConsecutiveFailures = 0
	} else {
		stream.ConsecutiveFailures++
		log.Warnf("Stream %s check failed: %s (failures: %d)", id, message, stream.ConsecutiveFailures)
	}

	// Update metrics
	if healthy {
		metrics.StreamStatus.WithLabelValues(id).Set(1)
	} else {
		metrics.StreamStatus.WithLabelValues(id).Set(0)
	}
}

// HTTP Handlers

func (m *Monitor) GetStreamsStatus(w http.ResponseWriter, r *http.Request) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	streams := make([]*types.Stream, 0, len(m.streams))
	for _, stream := range m.streams {
		streams = append(streams, stream)
	}

	respondJSON(w, http.StatusOK, streams)
}

func (m *Monitor) GetStreamStatus(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	m.mu.RLock()
	stream, exists := m.streams[id]
	m.mu.RUnlock()

	if !exists {
		respondError(w, http.StatusNotFound, "Stream not found")
		return
	}

	respondJSON(w, http.StatusOK, stream)
}

func (m *Monitor) CheckStream(w http.ResponseWriter, r *http.Request) {
	id := chi.URLParam(r, "id")

	m.mu.RLock()
	stream, exists := m.streams[id]
	m.mu.RUnlock()

	if !exists {
		respondError(w, http.StatusNotFound, "Stream not found")
		return
	}

	// Trigger immediate check
	m.wg.Add(1)
	go func() {
		defer m.wg.Done()
		m.checkStream(stream)
	}()

	respondJSON(w, http.StatusAccepted, map[string]string{
		"message": "Stream check initiated",
	})
}

func (m *Monitor) GetStats(w http.ResponseWriter, r *http.Request) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	total := len(m.streams)
	healthy := 0
	unhealthy := 0

	for _, stream := range m.streams {
		if stream.Healthy {
			healthy++
		} else {
			unhealthy++
		}
	}

	stats := map[string]interface{}{
		"total":     total,
		"healthy":   healthy,
		"unhealthy": unhealthy,
		"uptime":    time.Since(time.Now()).String(), // TODO: track actual uptime
	}

	respondJSON(w, http.StatusOK, stats)
}

// Helper functions

func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteStatus(status)
	// TODO: proper JSON encoding
}

func respondError(w http.ResponseWriter, status int, message string) {
	respondJSON(w, status, map[string]string{"error": message})
}
