# Ladybug TV - Project Structure

This document describes the complete project structure for Ladybug TV.

## Directory Structure

```
ladybug_tv/
├── .env.example                 # Environment variables template
├── .gitignore
├── README.md
├── PROJECT_STRUCTURE.md         # This file
├── pyproject.toml              # Python dependencies (uv format)
├── uv.lock
├── Taskfile.yml                # Task runner
├── docker-compose.yml          # Local development
├── docker-compose.prod.yml     # Production
├── alembic.ini
├── rxconfig.py                 # Reflex configuration
│
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│
├── assets/                     # Static assets
│   ├── favicon.ico
│   ├── logo.png
│   └── screenshots/
│
├── config/                     # Configuration files
│   ├── monitor.yaml           # Stream monitor config
│   ├── prometheus.yml         # Prometheus config
│   ├── nginx.conf             # Nginx config
│   └── grafana/
│       ├── dashboards/
│       └── datasources/
│
├── docker/                     # Docker configuration
│   ├── Dockerfile.reflex
│   ├── Dockerfile.reflex.prod
│   ├── Dockerfile.backend
│   ├── Dockerfile.backend.prod
│   ├── Dockerfile.stream
│   ├── Dockerfile.stream.prod
│   ├── Dockerfile.epg
│   ├── Dockerfile.epg.prod
│   └── init-db.sql
│
├── ladybug_tv/                 # Main Reflex app
│   ├── __init__.py
│   ├── ladybug_tv.py          # Main entry point
│   ├── components/            # Reusable UI components
│   │   ├── __init__.py
│   │   ├── video_player.py   # Custom HLS player
│   │   ├── channel_list.py   # Channel sidebar
│   │   ├── epg_display.py    # EPG components
│   │   └── navbar.py
│   ├── pages/                 # Page components
│   │   ├── __init__.py
│   │   ├── index.py          # Main TV viewer
│   │   ├── login.py
│   │   ├── settings.py
│   │   └── admin.py
│   ├── state/                 # State management
│   │   ├── __init__.py
│   │   ├── app_state.py      # Main app state
│   │   ├── auth_state.py     # Authentication
│   │   └── channel_state.py  # Channel management
│   └── utils/                 # Helper functions
│       ├── __init__.py
│       ├── api_client.py     # Backend API calls
│       └── constants.py
│
├── backend/                    # FastAPI backend services
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── channels.py
│   │       ├── streams.py
│   │       ├── epg.py
│   │       └── auth.py
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── channel.py
│   │   ├── epg.py
│   │   └── user.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── channel.py
│   │   ├── epg.py
│   │   └── user.py
│   └── services/              # Business logic
│       ├── __init__.py
│       ├── stream_service.py
│       ├── epg_service.py
│       └── auth_service.py
│
├── stream_relay/              # Stream processing service
│   ├── __init__.py
│   ├── server.py             # Stream relay server
│   ├── transcoder.py         # FFmpeg wrapper
│   └── hls_generator.py      # HLS playlist generator
│
├── epg_service/              # EPG processing
│   ├── __init__.py
│   ├── tasks.py              # Background tasks
│   ├── parser.py             # EPG XML parser
│   └── scheduler.py          # Update scheduler
│
├── stream_monitor/           # Go-based stream monitoring
│   ├── go.mod
│   ├── go.sum
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── cmd/
│   │   └── main.go           # Main entry point
│   ├── internal/
│   │   ├── monitor/          # Stream monitoring logic
│   │   │   └── monitor.go
│   │   ├── health/           # Health check handlers
│   │   │   └── health.go
│   │   └── metrics/          # Prometheus metrics
│   │       └── metrics.go
│   └── pkg/
│       ├── types/            # Shared types
│       │   └── types.go
│       └── config/           # Configuration
│           └── config.go
│
└── tests/                    # Test suite
    ├── __init__.py
    ├── unit/                 # Unit tests
    │   ├── test_state.py
    │   └── test_components.py
    ├── integration/          # Integration tests
    │   ├── test_api.py
    │   └── test_streams.py
    └── e2e/                  # End-to-end tests
        └── test_workflows.py
```

## Services Overview

### 1. Reflex App (Frontend/Backend)
- **Port**: 3000 (frontend), 8000 (backend)
- **Technology**: Python/Reflex
- **Purpose**: Main UI and application logic
- **Components**: Video player, channel list, EPG display

### 2. FastAPI Backend
- **Port**: 8001
- **Technology**: Python/FastAPI
- **Purpose**: RESTful API for channels, streams, EPG, and authentication
- **Database**: PostgreSQL

### 3. Stream Relay
- **Port**: 8080
- **Technology**: Python with FFmpeg
- **Purpose**: Handle stream transcoding and HLS generation
- **Features**: Adaptive bitrate streaming, format conversion

### 4. Stream Monitor (Go)
- **Ports**: 9090 (API), 9091 (metrics)
- **Technology**: Go
- **Purpose**: Monitor stream health and availability
- **Features**: 
  - Real-time stream health checks
  - Prometheus metrics export
  - RESTful API for stream status
  - Automatic failure detection

### 5. EPG Service
- **Technology**: Python
- **Purpose**: Electronic Program Guide data processing
- **Features**: XML parsing, scheduled updates, caching

### 6. PostgreSQL
- **Port**: 5432
- **Purpose**: Main database for channels, EPG, users

### 7. Redis
- **Port**: 6379
- **Purpose**: Caching and session management

### 8. Prometheus (Optional)
- **Port**: 9092
- **Purpose**: Metrics collection and monitoring

### 9. Grafana (Optional)
- **Port**: 3001
- **Purpose**: Metrics visualization

## Quick Start

### Development

```bash
# Start all services
task dev

# Or using docker-compose
docker-compose up

# Access services:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8001
# - Stream Monitor: http://localhost:9090
# - Metrics: http://localhost:9091/metrics
```

### Production

```bash
# Using production compose file
docker-compose -f docker-compose.prod.yml up -d

# With environment variables
export VERSION=v1.0.0
export DATABASE_URL=postgresql://user:pass@host:5432/db
docker-compose -f docker-compose.prod.yml up -d
```

## Stream Monitor API

The Go-based stream monitor provides the following endpoints:

### Health Checks
- `GET /health` - Service health
- `GET /ready` - Service readiness

### Stream Management
- `GET /api/v1/streams` - List all streams with status
- `GET /api/v1/streams/{id}` - Get specific stream status
- `POST /api/v1/streams/{id}/check` - Trigger immediate check
- `GET /api/v1/stats` - Get overall statistics

### Metrics
- `GET /metrics` (port 9091) - Prometheus metrics

## Configuration

### Environment Variables
See `.env.example` for all available configuration options.

### Config Files
- `config/monitor.yaml` - Stream monitor configuration
- `config/prometheus.yml` - Prometheus scrape configs
- `config/nginx.conf` - Nginx reverse proxy
- `rxconfig.py` - Reflex application config

## Development Tasks

```bash
# Install dependencies
task install

# Run development server
task dev

# Run tests
task test

# Build for production
task build:prod

# Deploy with Docker
task deploy:docker:build
task deploy:docker:run

# Run quality checks
task quality
```

## Monitoring

### Prometheus Metrics
The stream monitor exports the following metrics:

- `ladybug_stream_status` - Current stream status (1=healthy, 0=unhealthy)
- `ladybug_stream_check_success_total` - Total successful checks
- `ladybug_stream_check_failed_total` - Total failed checks
- `ladybug_stream_response_time_ms` - Response time histogram

### Grafana Dashboards
Pre-configured dashboards are available in `config/grafana/dashboards/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks: `task deploy:check`
5. Submit a pull request

## License

[Add your license here]
