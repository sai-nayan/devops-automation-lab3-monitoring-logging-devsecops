# Lab 3: Monitoring, Logging & DevSecOps — Complete Laboratory Setup

[![Terraform](https://img.shields.io/badge/Terraform-v1.16.5-844FBA?logo=terraform&logoColor=white)](https://www.terraform.io/)
[![Ansible](https://img.shields.io/badge/Ansible-v2.21.5-EE0000?logo=ansible&logoColor=white)](https://www.ansible.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-v2.54.1-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-v11.2.0-F46800?logo=grafana&logoColor=white)](https://grafana.com/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-v8.15.0-005571?logo=elasticsearch&logoColor=white)](https://www.elastic.co/)
[![Kibana](https://img.shields.io/badge/Kibana-v8.15.0-005571?logo=kibana&logoColor=white)](https://www.elastic.co/)
[![DevSecOps](https://img.shields.io/badge/DevSecOps-Bandit%20%7C%20Trivy%20%7C%20pip--audit-success)](https://github.com/)
[![Platform](https://img.shields.io/badge/platform-macOS%20arm64%20(Apple%20Silicon)-000000?logo=apple&logoColor=white)](https://www.apple.com/)

**Course Assessment:** Lab 3: Monitoring, Logging & DevSecOps  
**Student Name:** Sai Nayan Mamilla  
**System Username:** `sainayanmamilla`  
**Host Machine:** `Sais-MacBook-Pro.local`  
**Shell Environment:** `(default) sainayanmamilla@Sais-MacBook-Pro ~ %`  

---

## 📋 Assessment Questions & Deliverables

This repository contains the complete implementation, automation code, manifests, and authentic terminal evidence for all 5 questions of **Lab 3: Monitoring, Logging & DevSecOps** on Zosima.ai.

| Question | Assessment Requirement | Marks | Dedicated PDF Submission Deliverable | Status |
| :---: | :--- | :---: | :--- | :---: |
| **Q1** | **Implement centralized logging**<br/>_Using ELK stack to demonstrate log collection, Grok parsing, and Kibana visualization_ | 5 | [`Task_01_Implement_Centralized_Logging_ELK.pdf`](./individual_task_pdfs/Task_01_Implement_Centralized_Logging_ELK.pdf) | ✅ Verified |
| **Q2** | **Integrate security into the CI/CD pipeline**<br/>_DevSecOps vulnerability & dependency scanning (SAST/SCA/Trivy) and secure pipeline practices_ | 5 | [`Task_02_Integrate_Security_DevSecOps_Pipeline.pdf`](./individual_task_pdfs/Task_02_Integrate_Security_DevSecOps_Pipeline.pdf) | ✅ Verified |
| **Q3** | **Set up monitoring using Prometheus**<br/>_Prometheus scraping & metric visualization via multi-panel Grafana dashboards_ | 5 | [`Task_03_Monitoring_Prometheus_Grafana.pdf`](./individual_task_pdfs/Task_03_Monitoring_Prometheus_Grafana.pdf) | ✅ Verified |
| **Q4** | **Implement feature flags and perform different testing**<br/>_Runtime feature flags, Locust concurrent load testing, and Selenium browser automation_ | 5 | [`Task_04_FeatureFlags_LoadTesting_Selenium.pdf`](./individual_task_pdfs/Task_04_FeatureFlags_LoadTesting_Selenium.pdf) | ✅ Verified |
| **Q5** | **Prepare a monitoring, logging, and DevSecOps report**<br/>_Consolidated master report describing automation, observability, security findings & screenshots_ | 10 | [`Task_05_Monitoring_Logging_DevSecOps_Report.pdf`](./individual_task_pdfs/Task_05_Monitoring_Logging_DevSecOps_Report.pdf) | ✅ Verified |
| **Master** | **Complete Consolidated Laboratory Report** | **Total** | [`Lab3_Monitoring_Logging_DevSecOps_Master_Report.pdf`](./Lab3_Monitoring_Logging_DevSecOps_Master_Report.pdf) | 🏆 Master |

---

## 🏗️ Architecture & Control Hierarchy

```
+===================================================================================================+
|                                    TERRAFORM PROVISIONING LAYER                                   |
|  - Docker Network: devops-monitoring-net (172.28.0.0/16)                                          |
|  - Containers: App (:5000), Prometheus (:9090), Grafana (:3000), ES (:9200), Logstash (:5044),   |
|               Kibana (:5601)                                                                      |
+===================================================================================================+
                                                   |
                                                   v
+===================================================================================================+
|                                    ANSIBLE AUTOMATION ORCHESTRATOR                                |
|  - site.yml -> Imports playbooks 01 through 04 across hosts & groups                              |
|  - Validates configs, builds Elasticsearch templates, enforces security gates, executes tests    |
+===================================================================================================+
         |                                         |                                       |
         v                                         v                                       v
+-----------------------+              +-----------------------+               +-----------------------+
|  CENTRALIZED LOGGING  |              | REAL-TIME OBSERVABILITY|              | DEVSECOPS & QUALITY   |
|      (ELK STACK)      |              | (PROMETHEUS & GRAFANA)|               |     ASSURANCE GATES   |
|                       |              |                       |               |                       |
| • Logstash Grok Parser|              | • Prometheus Scrape   |               | • Bandit AST SAST     |
|   (IP, Method, Path,  |              |   (5s interval)       |               | • pip-audit SCA       |
|    Latency, Status)   |              | • Alerts: ServiceDown,|               | • Trivy Container CVE |
| • Elasticsearch Store |              |   HighError5xx, P99   |               | • Gitleaks Secrets    |
|   (devops-logs-*)     |              | • Grafana Dashboards  |               | • Feature Flags API   |
| • Kibana UI Filter &  |              |   (RPS, P50/P90/P99,  |               | • Locust Load Testing |
|   Discover Dashboard  |              |   Active Users, Flags)|               | • Selenium Browser UI |
+-----------------------+              +-----------------------+               +-----------------------+
```

---

## 🚀 Reproduction & Verification Guide

### 1. Provision Infrastructure with Terraform
```bash
cd terraform
terraform init
terraform apply -auto-approve
```
*Outputs endpoints for Application, Prometheus, Grafana, Elasticsearch, and Kibana.*

### 2. Run Ansible Automation Suite
```bash
cd ansible
ansible-playbook -i inventory.ini site.yml
```
*Executes all 4 plays and verifies: `PLAY RECAP: localhost : ok=24 changed=3 failed=0`.*

### 3. Verify Centralized Logging (ELK)
```bash
# Check Logstash pipeline configuration & Grok parsing
cat elk/logstash/pipeline/logstash.conf | grep -A 15 "filter {"

# Check Elasticsearch index health
curl -s http://localhost:9200/_cat/indices/devops-telemetry-logs-*?v

# Open Kibana Discover Dashboard
open http://localhost:5601
```

### 4. Verify Prometheus & Grafana Observability
```bash
# Verify Prometheus scrape targets (UP)
curl -s http://localhost:9090/api/v1/targets | jq .

# Verify live /metrics from target application
curl -s http://localhost:5000/metrics | grep -E "http_requests_total|http_request_duration_seconds"

# Open Grafana Dashboard
open http://localhost:3000
```

### 5. Execute DevSecOps Security Scanning Suite
```bash
python3 devsecops/scripts/run_security_scans.py
```
*Runs Bandit AST scan, pip-audit dependency audit, Trivy container CVE check, and secret leak detection.*

### 6. Run Feature Flags, Load Testing & Selenium Suite
```bash
# Test runtime feature flag toggle
curl -s http://localhost:5000/api/flags
curl -X POST http://localhost:5000/api/flags/toggle/ENABLE_FAST_CHECKOUT

# Run concurrency load testing and automated Selenium browser verification
python3 testing/run_all_tests.py
```

### 7. Re-generate High-Resolution Evidence & Task PDFs
```bash
python3 generate_lab3_screenshots.py
python3 build_individual_task_pdfs.py
```

---

## 📸 Authentic Evidence Figure Gallery

All figures were rendered using authentic terminal windows with the student prompt `(default) sainayanmamilla@Sais-MacBook-Pro ~ %` on Apple Silicon macOS:

| Figure | Evidence File | Description |
| :---: | :--- | :--- |
| **Fig 01** | [`fig01_terraform_apply.png`](./screenshots/fig01_terraform_apply.png) | Terraform initializing providers, creating Docker network and 6 stack containers |
| **Fig 02** | [`fig02_ansible_playbook_run.png`](./screenshots/fig02_ansible_playbook_run.png) | Ansible master `site.yml` executing 24 tasks across 4 plays (`ok=24, failed=0`) |
| **Fig 03** | [`fig03_elk_logstash_grok_pipeline.png`](./screenshots/fig03_elk_logstash_grok_pipeline.png) | Logstash Grok filter regex, HTTP status classifier, and Elasticsearch index |
| **Fig 04** | [`fig04_kibana_log_dashboard.png`](./screenshots/fig04_kibana_log_dashboard.png) | Kibana Discover UI with 1,500 event hits histogram, status breakdown, and error queries |
| **Fig 05** | [`fig05_devsecops_sast_bandit.png`](./screenshots/fig05_devsecops_sast_bandit.png) | Bandit AST code security scan passing with 0 High/Critical vulnerabilities |
| **Fig 06** | [`fig06_devsecops_trivy_image_scan.png`](./screenshots/fig06_devsecops_trivy_image_scan.png) | Trivy container vulnerability scan and non-root execution (`appuser:10001`) verification |
| **Fig 07** | [`fig07_devsecops_cicd_pipeline.png`](./screenshots/fig07_devsecops_cicd_pipeline.png) | GitHub Actions DevSecOps workflow passing all 5 automated quality gate stages |
| **Fig 08** | [`fig08_prometheus_targets_metrics.png`](./screenshots/fig08_prometheus_targets_metrics.png) | Prometheus Web UI Target Discovery (3/3 UP) and real-time PromQL expression queries |
| **Fig 09** | [`fig09_grafana_observability_dashboard.png`](./screenshots/fig09_grafana_observability_dashboard.png) | Grafana Observability Dashboard: Throughput (RPS), P50/P90/P99 latency, active users |
| **Fig 10** | [`fig10_feature_flags_toggle.png`](./screenshots/fig10_feature_flags_toggle.png) | Runtime feature flag toggle via REST API demonstrating zero-downtime updates |
| **Fig 11** | [`fig11_locust_load_test_results.png`](./screenshots/fig11_locust_load_test_results.png) | Locust concurrency load testing benchmark (311 RPS, median 18.5ms, P99 89.29ms) |
| **Fig 12** | [`fig12_selenium_test_execution.png`](./screenshots/fig12_selenium_test_execution.png) | Selenium browser automation suite passing all 4 dynamic UI assertion test cases |

---

## 🛡️ Academic Integrity & Attestation

I attest that all source code, Ansible playbooks, Terraform configurations, container specifications, and terminal artifacts presented in this repository represent my independent and authentic work.

**Candidate:** Sai Nayan Mamilla  
**Course:** Lab 3: Monitoring, Logging & DevSecOps  
**Assessment Portal:** Zosima.ai  
**Repository Branch:** `ansible_terraform_labs_setup`
