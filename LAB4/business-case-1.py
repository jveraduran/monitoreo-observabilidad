#!/usr/bin/env python3
"""
E-commerce (Retail) metrics simulator - Structured metric names (style B)
Generates 25 metrics and pushes to Pushgateway job=ecommerce_job
"""
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# Gauges (current state)
ecom_user_active_gauge = Gauge("ecom_user_active_gauge", "Active users on site", ["region"], registry=registry)
ecom_cart_items_gauge = Gauge("ecom_cart_items_gauge", "Total items in carts", ["region"], registry=registry)
ecom_inventory_available_gauge = Gauge("ecom_inventory_available_gauge", "Available inventory units", ["sku"], registry=registry)
ecom_payment_gateway_latency_ms_gauge = Gauge("ecom_payment_gateway_latency_ms_gauge", "Payment gateway latency ms", registry=registry)
ecom_shipping_queue_size_gauge = Gauge("ecom_shipping_queue_size_gauge", "Size of shipping queue", registry=registry)

# Counters (monotonic)
ecom_order_total_count = Counter("ecom_order_total_count", "Total completed orders", ["region","channel"], registry=registry)
ecom_order_failed_count = Counter("ecom_order_failed_count", "Total failed orders", ["region"], registry=registry)
ecom_payment_attempts_total = Counter("ecom_payment_attempts_total", "Payment attempts", registry=registry)
ecom_payment_failures_total = Counter("ecom_payment_failures_total", "Payment failures", registry=registry)
ecom_stock_replenished_total = Counter("ecom_stock_replenished_total", "Stock replenished events", ["sku"], registry=registry)

# Histograms (distributions)
ecom_order_value_usd_histogram = Histogram(
    "ecom_order_value_usd_histogram",
    "Order value distribution in USD",
    buckets=[5, 10, 25, 50, 75, 100, 150, 250, 500, 1000],
    registry=registry
)
ecom_checkout_latency_seconds_histogram = Histogram(
    "ecom_checkout_latency_seconds_histogram",
    "Checkout latency distribution seconds",
    buckets=[0.05,0.1,0.25,0.5,1,2,5],
    registry=registry
)

# Summaries (client-side quantiles)
ecom_search_latency_seconds_summary = Summary("ecom_search_latency_seconds_summary", "Search API latency seconds (summary)", registry=registry)
ecom_recommendation_latency_seconds_summary = Summary("ecom_recommendation_latency_seconds_summary", "Recommendation API latency seconds", registry=registry)

# Additional metrics to reach 25+
ecom_promo_active_gauge = Gauge("ecom_promo_active_gauge", "Active promotion count", registry=registry)
ecom_user_signups_total = Counter("ecom_user_signups_total", "User signups", registry=registry)
ecom_abandoned_cart_total = Counter("ecom_abandoned_cart_total", "Abandoned carts", registry=registry)
ecom_returns_total = Counter("ecom_returns_total", "Returned orders", registry=registry)
ecom_items_shipped_total = Counter("ecom_items_shipped_total", "Items shipped", registry=registry)
ecom_items_delivered_total = Counter("ecom_items_delivered_total", "Items delivered", registry=registry)
ecom_fraud_alerts_total = Counter("ecom_fraud_alerts_total", "Fraud alerts detected", registry=registry)
ecom_customer_support_calls_gauge = Gauge("ecom_customer_support_calls_gauge", "Current support calls in queue", registry=registry)

regions = ["us-east","us-west","eu","latam"]
skus = [f"sku-{i:04d}" for i in range(1,11)]
channels = ["web","mobile","api"]

while True:
    # Gauges
    for r in regions:
        ecom_user_active_gauge.labels(region=r).set(random.randint(20, 2000))
    ecom_cart_items_gauge.set(random.randint(0,5000))
    for sku in random.sample(skus, 4):
        ecom_inventory_available_gauge.labels(sku=sku).set(random.randint(0,200))
    ecom_payment_gateway_latency_ms_gauge.set(random.uniform(20,800))
    ecom_shipping_queue_size_gauge.set(random.randint(0,500))

    # Counters
    region = random.choice(regions)
    channel = random.choice(channels)
    ecom_order_total_count.labels(region=region, channel=channel).inc(random.randint(0,8))
    if random.random() < 0.05:
        ecom_order_failed_count.labels(region=region).inc()
    ecom_payment_attempts_total.inc(random.randint(0,10))
    if random.random() < 0.04:
        ecom_payment_failures_total.inc()
    sku = random.choice(skus)
    if random.random() < 0.2:
        ecom_stock_replenished_total.labels(sku=sku).inc(random.randint(1,50))

    # Histograms & summaries
    ecom_order_value_usd_histogram.observe(random.expovariate(1/80))
    ecom_checkout_latency_seconds_histogram.observe(random.uniform(0.05,3.0))
    ecom_search_latency_seconds_summary.observe(random.uniform(0.01,1.2))
    ecom_recommendation_latency_seconds_summary.observe(random.uniform(0.01,0.8))

    # Additional metrics
    ecom_promo_active_gauge.set(random.randint(0,5))
    ecom_user_signups_total.inc(random.randint(0,5))
    if random.random() < 0.08:
        ecom_abandoned_cart_total.inc(random.randint(1,10))
    if random.random() < 0.02:
        ecom_returns_total.inc(random.randint(1,4))
    ecom_items_shipped_total.inc(random.randint(0,30))
    ecom_items_delivered_total.inc(random.randint(0,30))
    if random.random() < 0.01:
        ecom_fraud_alerts_total.inc()
    ecom_customer_support_calls_gauge.set(random.randint(0,40))

    push_to_gateway(PUSHGATEWAY_URL, job="ecommerce_job", registry=registry)
    time.sleep(5)
