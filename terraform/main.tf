terraform {
  required_version = ">= 1.5.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4.0"
    }
  }
}

provider "docker" {}

# Isolated bridge network for telemetry and logging
resource "docker_network" "devops_network" {
  name   = "devops-monitoring-net"
  driver = "bridge"
  ipam_config {
    subnet = "172.28.0.0/16"
  }
}

# 1. Target Web Application Container
resource "docker_image" "app_image" {
  name = "devops-telemetry-app:v2.4"
  build {
    context = "${path.cwd}/../app"
    tag     = ["devops-telemetry-app:v2.4", "devops-telemetry-app:latest"]
  }
  keep_locally = true
}

resource "docker_container" "app" {
  name  = "target-telemetry-app"
  image = docker_image.app_image.image_id
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 5000
    external = var.app_port
  }
  env = [
    "ENV=production",
    "APP_NAME=telemetry-microservice",
    "PORT=5000"
  ]
  restart = "always"
}

# 2. Prometheus Monitoring Server
resource "docker_container" "prometheus" {
  name  = "prometheus-monitoring"
  image = "prom/prometheus:v2.54.1"
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 9090
    external = var.prometheus_port
  }
  volumes {
    host_path      = "${path.cwd}/../monitoring/prometheus/prometheus.yml"
    container_path = "/etc/prometheus/prometheus.yml"
  }
  command = [
    "--config.file=/etc/prometheus/prometheus.yml",
    "--storage.tsdb.path=/prometheus",
    "--web.enable-lifecycle"
  ]
  restart = "always"
}

# 3. Grafana Visualization Service
resource "docker_container" "grafana" {
  name  = "grafana-dashboard"
  image = "grafana/grafana:11.2.0"
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 3000
    external = var.grafana_port
  }
  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin",
    "GF_USERS_ALLOW_SIGN_UP=false"
  ]
  volumes {
    host_path      = "${path.cwd}/../monitoring/grafana/provisioning"
    container_path = "/etc/grafana/provisioning"
  }
  restart = "always"
}

# 4. Elasticsearch Engine (Single Node for Lab)
resource "docker_container" "elasticsearch" {
  name  = "elasticsearch-node"
  image = "elasticsearch:8.15.0"
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 9200
    external = var.elasticsearch_port
  }
  env = [
    "discovery.type=single-node",
    "xpack.security.enabled=false",
    "ES_JAVA_OPTS=-Xms512m -Xmx512m"
  ]
  restart = "always"
}

# 5. Logstash Processing Pipeline
resource "docker_container" "logstash" {
  name  = "logstash-pipeline"
  image = "logstash:8.15.0"
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 5044
    external = var.logstash_port
  }
  volumes {
    host_path      = "${path.cwd}/../elk/logstash/pipeline/logstash.conf"
    container_path = "/usr/share/logstash/pipeline/logstash.conf"
  }
  depends_on = [
    docker_container.elasticsearch
  ]
  restart = "always"
}

# 6. Kibana Centralized Logging Dashboard
resource "docker_container" "kibana" {
  name  = "kibana-dashboard"
  image = "kibana:8.15.0"
  networks_advanced {
    name = docker_network.devops_network.name
  }
  ports {
    internal = 5601
    external = var.kibana_port
  }
  env = [
    "ELASTICSEARCH_HOSTS=http://elasticsearch-node:9200"
  ]
  depends_on = [
    docker_container.elasticsearch
  ]
  restart = "always"
}
