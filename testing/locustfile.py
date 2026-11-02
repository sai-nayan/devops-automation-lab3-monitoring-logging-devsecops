from locust import HttpUser, task, between
import random

class DevOpsAppUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(5)
    def view_homepage(self):
        self.client.get("/")

    @task(3)
    def view_feature_flags_api(self):
        self.client.get("/api/flags")

    @task(4)
    def simulate_checkout(self):
        items = ["server_cluster", "database_replica", "monitoring_node", "edge_cdn"]
        self.client.get(f"/api/checkout?item={random.choice(items)}")

    @task(1)
    def trigger_occasional_error(self):
        # 1 in 13 requests triggers 500 error to generate realistic error telemetry
        with self.client.get("/api/error", catch_response=True) as response:
            if response.status_code == 500:
                response.success() # Expected behavior for test scenario
