FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install dependencies
RUN apk add --no-cache git

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o stream-monitor ./cmd

FROM alpine:latest

RUN apk --no-cache add ca-certificates wget

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/stream-monitor .

# Copy config
COPY config/monitor.yaml ./config/

EXPOSE 9090 9091

CMD ["./stream-monitor"]
