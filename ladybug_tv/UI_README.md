# 🐞 Ladybug TV

A modern, full-stack IPTV streaming platform built entirely in Python using Reflex for the frontend and FastAPI for backend services, with a Go-based stream monitoring service.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Reflex](https://img.shields.io/badge/Reflex-0.5+-purple.svg)](https://reflex.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Go](https://img.shields.io/badge/Go-1.21+-00ADD8.svg)](https://go.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📖 Overview

**Ladybug TV** is a self-hosted IPTV solution that provides a Netflix-like streaming experience for live television. Built with modern Python frameworks and a high-performance Go monitoring service, it demonstrates enterprise-grade DevOps practices.

### Key Features

- 📺 **Live TV Streaming** - HLS-based adaptive streaming
- 📋 **Channel Management** - Browse, search, and organize channels
- 📅 **EPG Integration** - Full electronic program guide
- ⭐ **Favorites System** - Save and quick-access favorite channels
- 🔍 **Search & Filter** - Find channels by name or category
- 📊 **Stream Monitoring** - Real-time health checks (Go service)
- 📈 **Metrics & Monitoring** - Prometheus + Grafana dashboards

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Ladybug TV                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌─────────────────┐             │
│  │   Reflex UI  │────────▶│   FastAPI       │             │
│  │  (Frontend)  │         │   (API Gateway) │             │
│  └──────────────┘         └────────┬────────┘             │
│                                    │                        │
│                  ┌─────────────────┴─────────────┐         │
│                  │                               │         │
│         ┌────────▼────────┐           ┌─────────▼──────┐  │
│         │  Stream Relay   │           │ EPG Service    │  │
│         │    (FFmpeg)     │           │  (Celery)      │  │
│         └────────┬────────┘           └─────────┬──────┘  │
│                  │                               │         │
│         ┌────────▼────────┐           ┌─────────▼──────┐  │
│         │ Stream Monitor  │           │     Redis      │  │
│         │      (Go)       │◄──────────│   (Cache)      │  │
│         └─────────────────┘           └────────────────┘  │
│                  │                                         │
│         ┌────────▼────────┐           ┌────────────────┐  │
│         │  Prometheus     │           │  PostgreSQL    │  │
│         │   (Metrics)     │           │   (Database)   │  │
│         └─────────────────┘           └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
ladybug_tv/
├── ladybug_tv/              # Reflex frontend
│   ├── components/          # UI components
│   │   ├── video_player.py
│   │   ├── channel_list.py
│   │   ├── epg_display.py
│   │   └── navbar.py
│   ├── pages/              # Page routes
│   │   ├── index.py
│   │   ├── login.py
│   │   └── settings.py
│   ├── state/              # State management
│   │   ├── app_state.py
│   │   ├── auth_state.py
│   │   └── channel_state.py
│   └── utils/              # Helper functions
│       ├── api_client.py
│       └── constants.py
│
├── backend/                # FastAPI backend
│   ├── api/v1/            # API endpoints
│   │   ├── channels.py
│   │   ├── streams.py
│   │   ├── epg.py
│   │   └── auth.py
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── config.py
│   └── main.py
│
├── stream_relay/          # Stream processing
│   ├── server.py
│   ├── transcoder.py
│   └── hls_generator.py
│
├── epg_service/           # EPG processing
│   ├── parser.py
│   └── tasks.py
│
├── monitor/               # Go stream monitor
│   ├── main.go
│   ├── go.mod
│   └── Dockerfile
│
├── config/                # Configuration
│   ├── channels.json
│   ├── epg.yaml
│   └── prometheus.yml
│
├── docker/                # Dockerfiles
├── k8s/                   # Kubernetes manifests
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── .github/workflows/     # CI/CD
└── docker-compose.yml
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Reflex)
- Docker & Docker Compose
- Go 1.21+ (optional, for monitor development)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ladybug_tv.git
cd ladybug_tv

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start with Docker Compose (recommended)
docker-compose up -d

# Or use Task runner
task docker
```

### Development Mode

```bash
# Start all services
task dev

# Or manually:
./scripts/start_dev.sh
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8001/docs
- **Metrics**: http://localhost:9091/metrics
- **Grafana**: http://localhost:3001

---

## 💻 Development

### Running Tests

```bash
# All tests
task test

# Python tests only
pytest

# Go tests
cd monitor && go test ./...
```

### Code Quality

```bash
# Format & lint
task lint

# Or manually:
black .
ruff check .
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
task migrate

# Seed sample data
task seed
```

---

## 🛠 Tech Stack

**Frontend**
- Reflex (Python web framework)
- HLS.js / Video.js

**Backend**
- FastAPI
- SQLAlchemy
- Celery
- Redis
- PostgreSQL

**Stream Processing**
- FFmpeg
- Go (stream monitor)

**DevOps**
- Docker / Docker Compose
- Kubernetes
- GitHub Actions
- Prometheus / Grafana

---

## 📊 Monitoring

The Go-based stream monitor provides:

- Real-time stream health checks
- Latency tracking
- Prometheus metrics export
- Redis-backed caching

Metrics available at `/metrics`:
- `stream_health` - Health status (1=healthy, 0=unhealthy)
- `stream_latency_ms` - Response latency
- `stream_checks_total` - Total checks performed

---

## 🐳 Docker Deployment

### Development

```bash
docker-compose up
```

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

---

## 🧪 Testing

```bash
# Run all tests with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html

# Run specific test file
pytest tests/unit/test_api.py
```

---

## 📚 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

### Key Endpoints

```
GET  /api/v1/channels          # List channels
GET  /api/v1/stream/{id}       # Get stream URL
GET  /api/v1/epg/{id}          # Get EPG data
POST /api/v1/auth/login        # Login
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Reflex](https://reflex.dev/) - Full-stack Python framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern API framework
- [FFmpeg](https://ffmpeg.org/) - Video processing

---

## 📞 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

**Built with ❤️ using Python & Go**
