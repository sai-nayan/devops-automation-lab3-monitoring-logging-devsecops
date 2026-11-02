import os
import json
import time
import uuid
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Configure Structured Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("DevOpsApp")

# Prometheus Metrics Definition
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Latency in Seconds",
    ["endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
FEATURE_FLAG_EVALS = Counter(
    "feature_flag_evaluations_total",
    "Total evaluations of feature flags",
    ["flag_name", "enabled"]
)
ACTIVE_USERS = Gauge(
    "app_active_users_current",
    "Current active simulated users on platform"
)

# Load Initial Feature Flags
FLAGS_FILE = os.path.join(os.path.dirname(__file__), "config", "feature_flags.json")
DEFAULT_FLAGS = {
    "ENABLE_BETA_UI": True,
    "ENABLE_DISCOUNT_BANNER": True,
    "ENABLE_FAST_CHECKOUT": False,
    "MAINTENANCE_MODE": False
}

def load_flags():
    if os.path.exists(FLAGS_FILE):
        try:
            with open(FLAGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_FLAGS.copy()
    return DEFAULT_FLAGS.copy()

def save_flags(flags):
    os.makedirs(os.path.dirname(FLAGS_FILE), exist_ok=True)
    with open(FLAGS_FILE, "w") as f:
        json.dump(flags, f, indent=2)

FEATURE_FLAGS = load_flags()

def log_structured_event(status_code, duration_ms, message, level="INFO"):
    log_payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "correlation_id": str(uuid.uuid4()),
        "client_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "method": request.method,
        "endpoint": request.path,
        "status_code": status_code,
        "latency_ms": round(duration_ms, 2),
        "user_agent": request.headers.get("User-Agent", "Unknown"),
        "level": level,
        "service": "telemetry-microservice",
        "environment": "production",
        "message": message
    }
    log_json = json.dumps(log_payload)
    if level == "ERROR":
        logger.error(log_json)
    elif level == "WARNING":
        logger.warning(log_json)
    else:
        logger.info(log_json)

@app.before_request
def before_request():
    request.start_time = time.time()
    ACTIVE_USERS.set(int(time.time()) % 45 + 10)

@app.after_request
def after_request(response):
    duration = time.time() - getattr(request, 'start_time', time.time())
    duration_ms = duration * 1000
    
    endpoint = request.endpoint or request.path
    status = str(response.status_code)
    
    # Avoid recording /metrics in metrics to prevent feedback loop
    if request.path != "/metrics":
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=status).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
        
        level = "INFO"
        if response.status_code >= 500:
            level = "ERROR"
        elif response.status_code >= 400:
            level = "WARNING"
            
        log_structured_event(response.status_code, duration_ms, f"Processed {request.method} {request.path}", level)
    
    return response

@app.route("/")
def home():
    flags = load_flags()
    for flag_name, is_enabled in flags.items():
        if isinstance(is_enabled, bool):
            FEATURE_FLAG_EVALS.labels(flag_name=flag_name, enabled=str(is_enabled)).inc()
            
    if flags.get("MAINTENANCE_MODE", False):
        return render_template("index.html", flags=flags), 503
        
    return render_template("index.html", flags=flags)

@app.route("/api/flags", methods=["GET"])
def get_flags():
    flags = load_flags()
    return jsonify({
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "feature_flags": flags
    })

@app.route("/api/flags/toggle/<flag_name>", methods=["POST", "GET"])
def toggle_flag(flag_name):
    flags = load_flags()
    if flag_name not in flags:
        return jsonify({"error": f"Flag '{flag_name}' not recognized"}), 404
        
    flags[flag_name] = not flags[flag_name]
    save_flags(flags)
    
    FEATURE_FLAG_EVALS.labels(flag_name=flag_name, enabled=str(flags[flag_name])).inc()
    return jsonify({
        "status": "updated",
        "flag": flag_name,
        "new_value": flags[flag_name],
        "all_flags": flags
    })

@app.route("/api/checkout", methods=["GET", "POST"])
def checkout():
    flags = load_flags()
    item = request.args.get("item", "standard_tier")
    time.sleep(0.04) # Simulate processing
    return jsonify({
        "status": "confirmed",
        "order_id": str(uuid.uuid4())[:8],
        "item": item,
        "fast_checkout_applied": flags.get("ENABLE_FAST_CHECKOUT", False),
        "discount_applied": flags.get("ENABLE_DISCOUNT_BANNER", False)
    })

@app.route("/api/error", methods=["GET"])
def trigger_error():
    time.sleep(0.02)
    return jsonify({
        "status": "error",
        "code": 500,
        "error_message": "Simulated unhandled database gateway timeout for observability testing",
        "trace_id": str(uuid.uuid4())
    }), 500

@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy", "service": "web-telemetry-app", "version": "2.4.0"})

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
