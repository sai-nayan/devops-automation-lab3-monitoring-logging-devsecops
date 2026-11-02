output "application_endpoint" {
  description = "Target application live URL"
  value       = "http://localhost:${var.app_port}"
}

output "application_metrics_endpoint" {
  description = "Prometheus scrape endpoint for application"
  value       = "http://localhost:${var.app_port}/metrics"
}

output "prometheus_ui_endpoint" {
  description = "Prometheus Web UI endpoint"
  value       = "http://localhost:${var.prometheus_port}"
}

output "grafana_dashboard_endpoint" {
  description = "Grafana Observability Portal"
  value       = "http://localhost:${var.grafana_port}"
}

output "elasticsearch_api_endpoint" {
  description = "Elasticsearch Cluster REST API"
  value       = "http://localhost:${var.elasticsearch_port}"
}

output "kibana_portal_endpoint" {
  description = "Kibana Log Visualization Portal"
  value       = "http://localhost:${var.kibana_port}"
}
