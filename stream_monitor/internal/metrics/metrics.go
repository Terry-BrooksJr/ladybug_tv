package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	StreamStatus = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "ladybug_stream_status",
			Help: "Current status of streams (1=healthy, 0=unhealthy)",
		},
		[]string{"stream_id"},
	)

	StreamCheckSuccess = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ladybug_stream_check_success_total",
			Help: "Total number of successful stream checks",
		},
		[]string{"stream_id"},
	)

	StreamCheckFailed = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "ladybug_stream_check_failed_total",
			Help: "Total number of failed stream checks",
		},
		[]string{"stream_id", "reason"},
	)

	StreamResponseTime = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "ladybug_stream_response_time_ms",
			Help:    "Stream response time in milliseconds",
			Buckets: prometheus.ExponentialBuckets(10, 2, 10),
		},
		[]string{"stream_id"},
	)
)

func Init() {
	// Register custom metrics if needed
}
