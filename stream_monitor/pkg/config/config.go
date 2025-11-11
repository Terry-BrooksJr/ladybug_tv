package config

import (
	"os"
	"gopkg.in/yaml.v3"
)

type Config struct {
	App     AppConfig     `yaml:"app"`
	Server  ServerConfig  `yaml:"server"`
	Monitor MonitorConfig `yaml:"monitor"`
	Metrics MetricsConfig `yaml:"metrics"`
	Log     LogConfig     `yaml:"log"`
}

type AppConfig struct {
	Name    string `yaml:"name"`
	Version string `yaml:"version"`
}

type ServerConfig struct {
	Host         string `yaml:"host"`
	Port         int    `yaml:"port"`
	ReadTimeout  int    `yaml:"read_timeout"`
	WriteTimeout int    `yaml:"write_timeout"`
}

type MonitorConfig struct {
	CheckInterval int `yaml:"check_interval"`
	Timeout       int `yaml:"timeout"`
	RetryAttempts int `yaml:"retry_attempts"`
}

type MetricsConfig struct {
	Host    string `yaml:"host"`
	Port    int    `yaml:"port"`
	Enabled bool   `yaml:"enabled"`
}

type LogConfig struct {
	Level  string `yaml:"level"`
	Format string `yaml:"format"`
}

func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}

	// Apply environment variable overrides
	applyEnvOverrides(&cfg)

	return &cfg, nil
}

func applyEnvOverrides(cfg *Config) {
	if host := os.Getenv("MONITOR_HOST"); host != "" {
		cfg.Server.Host = host
	}
	if port := os.Getenv("MONITOR_PORT"); port != "" {
		// Parse port
	}
	// Add more overrides as needed
}
