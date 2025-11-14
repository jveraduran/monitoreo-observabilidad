#!/usr/bin/env python3
"""
Este script envía múltiples tipos de métricas a un Pushgateway local para ser recolectadas por Prometheus.
Se incluyen ejemplos y explicaciones de:
- Counters
- Gauges
- Histograms
- Summaries
Además, se demuestra cómo se relacionan con diferentes tipos de consultas en PromQL.
"""

from prometheus_client import (
    CollectorRegistry,
    Gauge,
    Counter,
    Histogram,
    Summary,
    push_to_gateway,
)
import random
import time


PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()


# ===========================
# MÉTRICAS TIPO GAUGE
# ===========================
temperature = Gauge(
    "app_temperature_celsius",
    "Temperatura actual del sistema en grados Celsius",
    registry=registry,
)

cpu_usage = Gauge(
    "app_cpu_usage_percent",
    "Uso instantáneo de CPU en porcentaje",
    registry=registry,
)


# ===========================
# MÉTRICAS TIPO COUNTER
# ===========================
request_counter = Counter(
    "app_requests_total",
    "Conteo total de solicitudes atendidas por la aplicación",
    registry=registry,
)

error_counter = Counter(
    "app_errors_total",
    "Número total de errores ocurridos",
    registry=registry,
)


# ===========================
# MÉTRICAS TIPO HISTOGRAM
# ===========================
request_latency_hist = Histogram(
    "app_request_latency_seconds",
    "Latencia de solicitudes en segundos (histogram)",
    buckets=[0.1, 0.3, 0.5, 1.0, 2.0, 5.0],
    registry=registry,
)


# ===========================
# MÉTRICAS TIPO SUMMARY
# ===========================
processing_time_summary = Summary(
    "app_processing_time_seconds",
    "Tiempo de procesamiento (summary)",
    registry=registry,
)


# ===========================
# LOOP PRINCIPAL
# ===========================
while True:
    # GAUGE
    temperature.set(random.uniform(20.0, 35.0))
    cpu_usage.set(random.uniform(0, 100))

    # COUNTER
    request_counter.inc(random.randint(1, 5))
    if random.random() < 0.2:
        error_counter.inc()

    # HISTOGRAM
    request_latency_hist.observe(random.uniform(0.05, 3.0))

    # SUMMARY
    processing_time_summary.observe(random.uniform(0.01, 1.5))

    # PUSH AL PUSHGATEWAY
    push_to_gateway(PUSHGATEWAY_URL, job="app_metrics_job", registry=registry)

    time.sleep(5)
