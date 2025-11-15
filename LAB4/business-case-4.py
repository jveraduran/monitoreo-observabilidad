#!/usr/bin/env python3
"""
Telecom/ISP metrics simulator - Structured metric names (style B)
Generates 24+ metrics and pushes to Pushgateway job=telecom_job
"""
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# Gauges
isp_active_customers_gauge = Gauge("isp_active_customers_gauge", "Active connected customers", ["region"], registry=registry)
isp_average_latency_ms_gauge = Gauge("isp_average_latency_ms_gauge", "Average network latency ms", ["region"], registry=registry)
isp_current_bandwidth_mbps_gauge = Gauge("isp_current_bandwidth_mbps_gauge", "Current total bandwidth usage Mbps", registry=registry)

# Counters
isp_packets_dropped_total = Counter("isp_packets_dropped_total", "Total packets dropped", ["router"], registry=registry)
isp_outages_total = Counter("isp_outages_total", "Total outages recorded", registry=registry)
isp_reconnects_total = Counter("isp_reconnects_total", "Customer reconnect events", registry=registry)

# Histograms
isp_bandwidth_usage_mbps_histogram = Histogram(
    "isp_bandwidth_usage_mbps_histogram",
    "Bandwidth distribution in Mbps",
    buckets=[1,5,10,50,100,200,500,1000],
    registry=registry
)
isp_latency_ms_histogram = Histogram(
    "isp_latency_ms_histogram",
    "Latency distribution ms",
    buckets=[1,5,10,20,50,100,200,500],
    registry=registry
)

# Summaries
isp_repair_time_hours_summary = Summary("isp_repair_time_hours_summary", "Repair time hours summary", registry=registry)
isp_customer_complaints_total = Counter("isp_customer_complaints_total", "Customer complaints", registry=registry)

# Extra metrics
isp_peak_users_gauge = Gauge("isp_peak_users_gauge", "Peak concurrent users observed", registry=registry)
isp_routers_online_gauge = Gauge("isp_routers_online_gauge", "Routers online count", registry=registry)
isp_sla_violations_total = Counter("isp_sla_violations_total", "SLA violations", registry=registry)
isp_throughput_bytes_total = Counter("isp_throughput_bytes_total", "Total throughput bytes", registry=registry)
isp_connection_errors_total = Counter("isp_connection_errors_total", "Connection errors total", registry=registry)
isp_avg_jitter_ms_gauge = Gauge("isp_avg_jitter_ms_gauge", "Average jitter ms", registry=registry)

regions = ["north","south","east","west"]
routers = ["r1","r2","r3","core"]

while True:
    for r in regions:
        isp_active_customers_gauge.labels(region=r).set(random.randint(10000,90000))
        isp_average_latency_ms_gauge.labels(region=r).set(random.uniform(5,120))
    isp_current_bandwidth_mbps_gauge.set(random.uniform(100,5000))

    for rt in routers:
        isp_packets_dropped_total.labels(router=rt).inc(random.randint(0,500))
    if random.random() < 0.02:
        isp_outages_total.inc()
        isp_repair_time_hours_summary.observe(random.uniform(0.5,24))
    isp_reconnects_total.inc(random.randint(0,300))
    isp_bandwidth_usage_mbps_histogram.observe(random.uniform(1,800))
    isp_latency_ms_histogram.observe(random.uniform(1,400))
    isp_customer_complaints_total.inc(random.randint(0,5))
    isp_peak_users_gauge.set(random.randint(20000,120000))
    isp_routers_online_gauge.set(random.randint(4,12))
    if random.random() < 0.01:
        isp_sla_violations_total.inc()
    isp_throughput_bytes_total.inc(random.randint(1000,1000000))
    isp_connection_errors_total.inc(random.randint(0,50))
    isp_avg_jitter_ms_gauge.set(random.uniform(0.1,30))

    push_to_gateway(PUSHGATEWAY_URL, job="telecom_job", registry=registry)
    time.sleep(5)
