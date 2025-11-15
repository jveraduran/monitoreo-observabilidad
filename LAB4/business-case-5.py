#!/usr/bin/env python3
"""
saas_push.py

Simulador de métricas de plataforma SaaS que hace PUSH aditivo a Pushgateway.
Genera métricas de rendimiento, errores, infraestructura y negocio de forma
continua usando pushadd_to_gateway.

Requisitos:
    pip install prometheus_client

Uso:
    python3 saas_push.py --instance <instance-name> --pushgateway http://localhost:9091 --interval 5
"""

import time
import random
import argparse
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, pushadd_to_gateway

def build_registry(registry):
    # 1. Rendimiento y Latencia (Gauges, Histograms, Summaries)
    registry.saas_active_sessions_gauge = Gauge(
        "saas_active_sessions_gauge", "Active user sessions", registry=registry
    )
    registry.saas_api_latency_ms_gauge = Gauge(
        "saas_api_latency_ms_gauge", "API latency ms (instantaneous)", ["endpoint"], registry=registry
    )
    registry.saas_request_duration_seconds_histogram = Histogram(
        "saas_request_duration_seconds_histogram",
        "Request duration seconds (end-to-end)",
        buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5, float('inf')],
        registry=registry
    )
    registry.saas_db_query_seconds_summary = Summary(
        "saas_db_query_seconds_summary", "DB query duration summary", registry=registry
    )
    registry.saas_cache_hit_ratio_gauge = Gauge(
        "saas_cache_hit_ratio_gauge", "Cache hit ratio", ["endpoint"], registry=registry
    )
    registry.saas_stream_bytes_total = Counter(
        "saas_stream_bytes_total", "Stream bytes processed", registry=registry
    )

    # 2. Errores y Calidad (Counters & Gauges)
    registry.saas_api_requests_total_counter = Counter(
        "saas_api_requests_total_counter", "API requests total", ["endpoint", "method", "code"], registry=registry
    )
    registry.saas_errors_total_counter = Counter(
        "saas_errors_total_counter", "Internal/Application errors total", ["endpoint"], registry=registry
    )
    registry.saas_error_rate_5m_gauge = Gauge(
        "saas_error_rate_5m_gauge", "Approx error rate over 5m (derived)", registry=registry
    )

    # 3. Infraestructura y DevOps (Gauges & Counters)
    registry.saas_instance_cpu_percent_gauge = Gauge(
        "saas_instance_cpu_percent_gauge", "Instance CPU percent", ["instance_id"], registry=registry
    )
    registry.saas_instance_memory_mb_gauge = Gauge(
        "saas_instance_memory_mb_gauge", "Instance memory MB", ["instance_id"], registry=registry
    )
    registry.saas_db_connections_gauge = Gauge(
        "saas_db_connections_gauge", "DB connections in use", registry=registry
    )
    registry.saas_deployments_total = Counter(
        "saas_deployments_total", "Deployments total", registry=registry
    )
    registry.saas_background_jobs_pending_gauge = Gauge(
        "saas_background_jobs_pending_gauge", "Background jobs pending", registry=registry
    )

    # 4. Negocio y Crecimiento (Counters & Gauges)
    registry.saas_user_signup_total = Counter(
        "saas_user_signup_total", "User signups total", registry=registry
    )
    registry.saas_password_reset_total = Counter(
        "saas_password_reset_total", "Password resets total", registry=registry
    )
    registry.saas_feature_flag_active_gauge = Gauge(
        "saas_feature_flag_active_gauge", "Feature flags active (0/1)", ["flag"], registry=registry
    )

    return registry

def simulate_and_push(args):
    registry = CollectorRegistry()
    registry = build_registry(registry)

    endpoints = ["/login", "/search", "/billing", "/upload", "/report"]
    instances = [f"i-{i:03d}" for i in range(1, 8)]

    while True:
        # --- 1. Rendimiento y Latencia ---
        registry.saas_active_sessions_gauge.set(random.randint(100, 5000))
        
        for ep in endpoints:
            # Latency Gauge (instantaneous sample)
            registry.saas_api_latency_ms_gauge.labels(endpoint=ep).set(random.uniform(10, 700))
            
            # Cache Hit Ratio Gauge
            registry.saas_cache_hit_ratio_gauge.labels(endpoint=ep).set(random.uniform(0.4, 0.99))
            
            # Requests and Duration (Counters, Histograms, Summaries)
            get_reqs = random.randint(10, 500)
            post_reqs = random.randint(0, 200)
            
            # Successful Requests
            registry.saas_api_requests_total_counter.labels(endpoint=ep, method="GET", code="200").inc(get_reqs)
            registry.saas_api_requests_total_counter.labels(endpoint=ep, method="POST", code="200").inc(post_reqs)

            for _ in range(get_reqs + post_reqs):
                registry.saas_request_duration_seconds_histogram.observe(random.uniform(0.01, 2.5))
                registry.saas_db_query_seconds_summary.observe(random.uniform(0.001, 0.5))

        registry.saas_stream_bytes_total.inc(random.randint(1000, 500000))

        # --- 2. Errores y Calidad ---
        error_count = 0
        for ep in endpoints:
            if random.random() < 0.03:
                app_errors = random.randint(1, 5)
                registry.saas_errors_total_counter.labels(endpoint=ep).inc(app_errors)
                error_count += app_errors
                # Also log API 5xx errors
                registry.saas_api_requests_total_counter.labels(endpoint=ep, method="GET", code="500").inc(random.randint(0, 2))
        
        # Approximate Error Rate (This would normally be calculated in Prometheus)
        # We simulate the final output of a PromQL query for demonstration.
        registry.saas_error_rate_5m_gauge.set(random.uniform(0.0, 5.0)) # Rate in errors per 1000 requests

        # --- 3. Infraestructura y DevOps ---
        for inst in instances:
            registry.saas_instance_cpu_percent_gauge.labels(instance_id=inst).set(random.uniform(1, 95))
            registry.saas_instance_memory_mb_gauge.labels(instance_id=inst).set(random.uniform(200, 32000))
        
        registry.saas_deployments_total.inc(random.randint(0, 1))
        registry.saas_background_jobs_pending_gauge.set(random.randint(0, 120))
        registry.saas_db_connections_gauge.set(random.randint(20, 500))

        # --- 4. Negocio y Crecimiento ---
        registry.saas_user_signup_total.inc(random.randint(0, 20))
        registry.saas_password_reset_total.inc(random.randint(0, 5))
        registry.saas_feature_flag_active_gauge.labels(flag="beta_ui").set(random.choice([0, 1]))
        registry.saas_feature_flag_active_gauge.labels(flag="new_pricing").set(1)


        # --- Push al Pushgateway ---
        instance = args.instance or "saas-sim-app-1"
        try:
            pushadd_to_gateway(
                args.pushgateway,
                job=args.job,
                registry=registry,
                grouping_key={"instance": instance}
            )
            print(f"Pushed metrics to {args.pushgateway} (job={args.job}, instance={instance}) at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error pushing to Pushgateway: {e}")

        time.sleep(args.interval)

def main():
    parser = argparse.ArgumentParser(description="SaaS metrics simulator (push to Pushgateway)")
    parser.add_argument("--pushgateway", default="http://localhost:9091", help="Pushgateway URL")
    parser.add_argument("--job", default="saas_job", help="Pushgateway job name")
    parser.add_argument("--instance", default="saas-sim-app-1", help="Instance label to push (grouping_key)")
    parser.add_argument("--interval", type=int, default=5, help="Seconds between pushes")
    args = parser.parse_args()

    simulate_and_push(args)

if __name__ == "__main__":
    main()