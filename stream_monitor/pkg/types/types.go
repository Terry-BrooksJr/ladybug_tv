package types

import "time"

type Stream struct {
	ID                  string    `json:"id"`
	Name                string    `json:"name"`
	URL                 string    `json:"url"`
	Healthy             bool      `json:"healthy"`
	LastCheck           time.Time `json:"last_check"`
	LastMessage         string    `json:"last_message"`
	ResponseTime        int64     `json:"response_time_ms"`
	ConsecutiveFailures int       `json:"consecutive_failures"`
}

type StreamCheckResult struct {
	StreamID     string `json:"stream_id"`
	Success      bool   `json:"success"`
	ResponseTime int64  `json:"response_time_ms"`
	Error        string `json:"error,omitempty"`
	Timestamp    time.Time `json:"timestamp"`
}
