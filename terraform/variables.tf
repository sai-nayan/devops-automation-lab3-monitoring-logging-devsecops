variable "app_port" {
  description = "Port exposed by the Flask telemetry application"
  type        = number
  default     = 5000
}

variable "prometheus_port" {
  description = "Port exposed by Prometheus Web UI and API"
  type        = number
  default     = 9090
}

variable "grafana_port" {
  description = "Port exposed by Grafana Observability Dashboard"
  type        = number
  default     = 3000
}

variable "elasticsearch_port" {
  description = "Port exposed by Elasticsearch REST API"
  type        = number
  default     = 9200
}

variable "kibana_port" {
  description = "Port exposed by Kibana Dashboard UI"
  type        = number
  default     = 5601
}

variable "logstash_port" {
  description = "Port exposed by Logstash beats/http receiver"
  type        = number
  default     = 5044
}

variable "environment" {
  description = "Deployment target environment tier"
  type        = string
  default     = "production"
}
