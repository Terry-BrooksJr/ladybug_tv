# Stream Monitor Service

Go-based microservice for monitoring stream health and availability.

## Features

- Concurrent health checks for multiple streams
- Prometheus metrics export
- Redis integration for caching
- Configurable check intervals
- Latency tracking

## Metrics

- `stream_health` - Stream health status (1=healthy, 0=unhealthy)
- `stream_latency_ms` - Stream response latency
- `stream_checks_total` - Total health checks performed

## Running

```bash
# Development
go run main.go

# Build
go build -o monitor

# Docker
docker build -t ladybug-tv-monitor .
docker run -e REDIS_URL=redis://redis:6379 ladybug-tv-monitor
```

## Environment Variables

- `REDIS_URL` - Redis connection string (default: redis://localhost:6379)
- `STREAM_BASE_URL` - Base URL for streams (default: http://localhost:8002)
- `METRICS_PORT` - Port for Prometheus metrics (default: 9091)
