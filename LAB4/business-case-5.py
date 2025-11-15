#!/usr/bin/env python3
"""
SaaS platform metrics simulator - Structured metric names (style B)
Generates 24+ metrics and pushes to Pushgateway job=saas_job
"""
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# Gauges
saas_api_latency_ms_gauge = Gauge("saas_api_latency_ms_gauge", "API latency ms", ["endpoint"], registry=registry)
saas_active_sessions_gauge = Gauge("saas_active_sessions_gauge", "Active user sessions", registry=registry)
saas_instance_cpu_percent_gauge = Gauge("saas_instance_cpu_percent_gauge", "Instance CPU percent", ["instance_id"], registry=registry)
saas_instance_memory_mb_gauge = Gauge("saas_instance_memory_mb_gauge", "Instance memory MB", ["instance_id"], registry=registry)

# Counters
saas_api_requests_total_counter = Counter("saas_api_requests_total_counter", "API requests total", ["endpoint","method"], registry=registry)
saas_errors_total_counter = Counter("saas_errors_total_counter", "API errors total", ["endpoint"], registry=registry)
saas_deployments_total = Counter("saas_deployments_total", "Deployments total", registry=registry)

# Histograms
saas_request_duration_seconds_histogram = Histogram(
    "saas_request_duration_seconds_histogram",
    "Request duration seconds",
    buckets=[0.01,0.05,0.1,0.3,0.5,1,2,5],
    registry=registry
)

# Summaries
saas_db_query_seconds_summary = Summary("saas_db_query_seconds_summary", "DB query duration summary", registry=registry)

# Extra metrics to reach 20+
endpoints = ["/login","/search","/billing","/upload","/report"]
instances = [f"i-{i:03d}" for i in range(1,8)]

saas_cache_hit_ratio_gauge = Gauge("saas_cache_hit_ratio_gauge", "Cache hit ratio", ["endpoint"], registry=registry)
saas_background_jobs_pending_gauge = Gauge("saas_background_jobs_pending_gauge", "Background jobs pending", registry=registry)
saas_feature_flag_active_gauge = Gauge("saas_feature_flag_active_gauge", "Feature flags active", ["flag"], registry=registry)
saas_user_signup_total = Counter("saas_user_signup_total", "User signups total", registry=registry)
saas_password_reset_total = Counter("saas_password_reset_total", "Password resets total", registry=registry)
saas_db_connections_gauge = Gauge("saas_db_connections_gauge", "DB connections in use", registry=registry)
saas_stream_bytes_total = Counter("saas_stream_bytes_total", "Stream bytes processed", registry=registry)
saas_error_rate_5m_gauge = Gauge("saas_error_rate_5m_gauge", "Approx error rate over 5m (approx)", registry=registry)

while True:
    saas_active_sessions_gauge.set(random.randint(100,5000))
    for ep in endpoints:
        saas_api_latency_ms_gauge.labels(endpoint=ep).set(random.uniform(10,700))
        saas_api_requests_total_counter.labels(endpoint=ep, method="GET").inc(random.randint(10,500))
        saas_api_requests_total_counter.labels(endpoint=ep, method="POST").inc(random.randint(0,200))
        if random.random() < 0.03:
            saas_errors_total_counter.labels(endpoint=ep).inc()
        saas_cache_hit_ratio_gauge.labels(endpoint=ep).set(random.uniform(0.4,0.99))
        saas_request_duration_seconds_histogram.observe(random.uniform(0.01,2.5))
        saas_db_query_seconds_summary.observe(random.uniform(0.001,0.5))
    for inst in instances:
        saas_instance_cpu_percent_gauge.labels(instance_id=inst).set(random.uniform(1,95))
        saas_instance_memory_mb_gauge.labels(instance_id=inst).set(random.uniform(200,32000))
    saas_deployments_total.inc(random.randint(0,1))
    saas_background_jobs_pending_gauge.set(random.randint(0,120))
    saas_feature_flag_active_gauge.labels(flag="beta_ui").set(random.choice([0,1]))
    saas_user_signup_total.inc(random.randint(0,20))
    saas_password_reset_total.inc(random.randint(0,5))
    saas_db_connections_gauge.set(random.randint(20,500))
    saas_stream_bytes_total.inc(random.randint(1000,500000))
    saas_error_rate_5m_gauge.set(random.uniform(0,5))

    push_to_gateway(PUSHGATEWAY_URL, job="saas_job", registry=registry)
    time.sleep(5)
