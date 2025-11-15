#!/usr/bin/env python3
"""
ecommerce_push.py

Simulador de métricas e-commerce que hace PUSH a Pushgateway.
Genera métricas (counters, gauges, histograms, summaries) y las envía usando
pushadd_to_gateway para no sobrescribir series previas.

Requisitos:
    pip install prometheus_client

Uso:
    python3 ecommerce_push.py --instance <instance-name> --pushgateway http://localhost:9091 --interval 5
"""

import time
import random
import argparse
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, Summary, pushadd_to_gateway

def build_registry(registry):
    # Business / Sales
    registry.ecom_orders_total = Counter(
        "ecom_orders_total", "Total de órdenes creadas", ["region", "channel"], registry=registry
    )
    registry.ecom_orders_paid_total = Counter(
        "ecom_orders_paid_total", "Órdenes pagadas exitosamente", ["region", "channel"], registry=registry
    )
    registry.ecom_orders_failed_total = Counter(
        "ecom_orders_failed_total", "Órdenes fallidas", ["region", "channel"], registry=registry
    )
    registry.ecom_revenue_total = Counter(
        "ecom_revenue_total", "Revenue total en cents (integer)", ["region"], registry=registry
    )
    registry.ecom_items_sold_total = Counter(
        "ecom_items_sold_total", "Ítems vendidos", ["sku", "region"], registry=registry
    )
    registry.ecom_cart_created_total = Counter(
        "ecom_cart_created_total", "Carritos creados", ["region"], registry=registry
    )
    registry.ecom_cart_abandoned_total = Counter(
        "ecom_cart_abandoned_total", "Carritos abandonados", ["region"], registry=registry
    )

    # Payments
    registry.payment_request_total = Counter(
        "payment_request_total", "Intentos de pago", ["gateway"], registry=registry
    )
    registry.payment_success_total = Counter(
        "payment_success_total", "Pagos completados", ["gateway"], registry=registry
    )
    registry.payment_failed_total = Counter(
        "payment_failed_total", "Pagos rechazados", ["gateway"], registry=registry
    )
    registry.payment_processing_latency_seconds = Histogram(
        "payment_processing_latency_seconds", "Latencia de procesamiento de pagos", buckets=[0.05,0.1,0.25,0.5,1,2,5], registry=registry
    )

    # Checkout funnel
    registry.funnel_step_total = Counter(
        "funnel_step_total", "Eventos por paso del funnel", ["step", "region"], registry=registry
    )

    # Logistics
    registry.shipping_order_dispatched_total = Counter(
        "shipping_order_dispatched_total", "Órdenes despachadas", ["region"], registry=registry
    )
    registry.shipping_order_delivered_total = Counter(
        "shipping_order_delivered_total", "Órdenes entregadas", ["region"], registry=registry
    )
    registry.shipping_time_seconds = Histogram(
        "shipping_time_seconds", "Tiempo despacho→entrega", buckets=[3600, 7200, 14400, 28800, 86400], registry=registry
    )
    registry.warehouse_inventory = Gauge(
        "warehouse_inventory", "Stock actual por producto", ["sku", "region"], registry=registry
    )

    # Backend / infra
    registry.api_requests_total = Counter(
        "api_requests_total", "API requests totales", ["service","code"], registry=registry
    )
    registry.api_errors_total = Counter(
        "api_errors_total", "API errores 4xx/5xx", ["service","code"], registry=registry
    )
    registry.api_latency_seconds = Histogram(
        "api_latency_seconds", "Latencia endpoints", buckets=[0.005,0.02,0.05,0.1,0.25,0.5,1,2], registry=registry
    )
    registry.queue_processing_size = Gauge(
        "queue_processing_size", "Tamaño de la cola de procesamiento", ["queue"], registry=registry
    )
    registry.db_query_time_seconds = Histogram(
        "db_query_time_seconds", "Latencia de consultas DB", buckets=[0.001,0.005,0.01,0.05,0.1,0.5], registry=registry
    )

    # Frontend / UX
    registry.frontend_page_load_seconds = Histogram(
        "frontend_page_load_seconds", "Page load / TTFB", buckets=[0.1,0.5,1,2,5], registry=registry
    )
    registry.frontend_js_errors_total = Counter(
        "frontend_js_errors_total", "Errores JS en frontend", ["page"], registry=registry
    )

    # Fraud & security
    registry.fraud_alerts_total = Counter(
        "fraud_alerts_total", "Alertas de fraude", ["region"], registry=registry
    )
    registry.login_failed_total = Counter(
        "login_failed_total", "Intentos fallidos de login", ["region"], registry=registry
    )
    registry.login_success_total = Counter(
        "login_success_total", "Logins exitosos", ["region"], registry=registry
    )

    # DevOps
    registry.cpu_usage_percent = Gauge(
        "cpu_usage_percent", "Uso de CPU percentual", ["instance"], registry=registry
    )
    registry.memory_usage_bytes = Gauge(
        "memory_usage_bytes", "Uso de memoria en bytes", ["instance"], registry=registry
    )
    registry.fs_free_bytes = Gauge(
        "fs_free_bytes", "Espacio libre en bytes", ["instance","mountpoint"], registry=registry
    )
    registry.pod_restarts_total = Counter(
        "pod_restarts_total", "Reinicios de contenedores", ["pod"], registry=registry
    )

    # Misc / business derived (gauges updated by script)
    registry.ecom_conversion_rate = Gauge(
        "ecom_conversion_rate", "Conversion rate (orders/cart) - instant", ["region"], registry=registry
    )
    registry.ecom_avg_order_value = Gauge(
        "ecom_avg_order_value", "Average order value (USD)", ["region"], registry=registry
    )

    return registry

def simulate_and_push(args):
    registry = CollectorRegistry()
    registry = build_registry(registry)

    regions = ["us-east","us-west","eu","latam"]
    channels = ["web","mobile","api"]
    skus = [f"sku-{i:04d}" for i in range(1,21)]
    gateways = ["stripe","paypal","internal"]

    # Simple state to compute AOV and conversion
    revenue_by_region = {r: 0 for r in regions}
    orders_by_region = {r: 0 for r in regions}
    carts_by_region = {r: 0 for r in regions}

    while True:
        # Simulate business events
        for r in regions:
            # carts and conversion events
            carts = random.randint(5, 40)
            carts_by_region[r] += carts
            registry.ecom_cart_created_total.labels(region=r).inc(carts)

            abandoned = int(carts * random.uniform(0.05, 0.35))
            registry.ecom_cart_abandoned_total.labels(region=r).inc(abandoned)

            # funnel steps
            registry.funnel_step_total.labels(step="product_view", region=r).inc(random.randint(20,100))
            registry.funnel_step_total.labels(step="cart", region=r).inc(carts)
            registry.funnel_step_total.labels(step="checkout", region=r).inc(int(carts * random.uniform(0.3,0.9)))

            # orders
            for ch in channels:
                completed = random.randint(0, 6)
                registry.ecom_orders_total.labels(region=r, channel=ch).inc(completed)
                paid = int(completed * random.uniform(0.7, 1.0))
                registry.ecom_orders_paid_total.labels(region=r, channel=ch).inc(paid)
                failed = completed - paid
                if failed > 0:
                    registry.ecom_orders_failed_total.labels(region=r, channel=ch).inc(failed)

                # revenue (in cents)
                for _ in range(paid):
                    value_cents = random.randint(1500, 25000)  # $15 - $250
                    registry.ecom_revenue_total.labels(region=r).inc(value_cents)
                    revenue_by_region[r] += value_cents
                    orders_by_region[r] += 1
                    # items sold
                    sku = random.choice(skus)
                    qty = random.randint(1,4)
                    registry.ecom_items_sold_total.labels(sku=sku, region=r).inc(qty)

            # shipping
            dispatched = random.randint(0, 10)
            registry.shipping_order_dispatched_total.labels(region=r).inc(dispatched)
            delivered = int(dispatched * random.uniform(0.6, 0.99))
            registry.shipping_order_delivered_total.labels(region=r).inc(delivered)
            for _ in range(delivered):
                registry.shipping_time_seconds.observe(random.uniform(3600, 86400))

            # fraud/login
            if random.random() < 0.02:
                registry.fraud_alerts_total.labels(region=r).inc()
            registry.login_failed_total.labels(region=r).inc(random.randint(0,3))
            registry.login_success_total.labels(region=r).inc(random.randint(0,20))

            # update inventory gauges for a few skus
            for sku in random.sample(skus, 4):
                registry.warehouse_inventory.labels(sku=sku, region=r).set(random.randint(0,500))

            # compute derived gauges
            orders = orders_by_region[r] if orders_by_region[r] > 0 else 0
            carts_count = carts_by_region[r] if carts_by_region[r] > 0 else 1
            aov = (revenue_by_region[r] / 100.0) / orders_by_region[r] if orders_by_region[r] > 0 else 0.0
            conv = orders_by_region[r] / carts_by_region[r] if carts_by_region[r] > 0 else 0.0
            registry.ecom_avg_order_value.labels(region=r).set(round(aov,2))
            registry.ecom_conversion_rate.labels(region=r).set(round(conv,4))

        # infra / backend metrics (simulated)
        instance = args.instance or "ecommerce-sim-1"
        registry.cpu_usage_percent.labels(instance=instance).set(random.uniform(2, 92))
        registry.memory_usage_bytes.labels(instance=instance).set(random.randint(200_000_000, 6_000_000_000))
        registry.fs_free_bytes.labels(instance=instance, mountpoint="/").set(random.randint(5_000_000_000, 200_000_000_000))
        registry.queue_processing_size.labels(queue="orders").set(random.randint(0, 120))
        registry.db_query_time_seconds.observe(random.uniform(0.0005, 0.05))

        # API metrics
        for svc in ["orders","checkout","users"]:
            reqs = random.randint(0, 200)
            errors = int(reqs * random.uniform(0.0, 0.02))
            registry.api_requests_total.labels(service=svc, code="200").inc(reqs - errors)
            if errors > 0:
                registry.api_errors_total.labels(service=svc, code="500").inc(errors)
            # latency samples
            for _ in range(min(reqs, 5)):
                registry.api_latency_seconds.observe(random.uniform(0.002, 1.2))

        # frontend metrics
        registry.frontend_page_load_seconds.observe(random.uniform(0.1, 3.5))
        if random.random() < 0.03:
            registry.frontend_js_errors_total.labels(page="/checkout").inc()

        # payments
        gateway = random.choice(gateways)
        pay_attempts = random.randint(0, 30)
        registry.payment_request_total.labels(gateway=gateway).inc(pay_attempts)
        successes = int(pay_attempts * random.uniform(0.85,0.99))
        registry.payment_success_total.labels(gateway=gateway).inc(successes)
        failures = pay_attempts - successes
        if failures > 0:
            registry.payment_failed_total.labels(gateway=gateway).inc(failures)
        for _ in range(min(5, pay_attempts)):
            registry.payment_processing_latency_seconds.observe(random.uniform(0.02, 3.0))

        # push to pushgateway using pushadd (no overwrite)
        try:
            pushadd_to_gateway(
                args.pushgateway,
                job=args.job,
                registry=registry,
                grouping_key={"instance": instance}
            )
            print(f"Pushed metrics to {args.pushgateway} (job={args.job}, instance={instance})")
        except Exception as e:
            print("Error pushing to Pushgateway:", e)

        time.sleep(args.interval)

def main():
    parser = argparse.ArgumentParser(description="Ecommerce metrics simulator (push to Pushgateway)")
    parser.add_argument("--pushgateway", default="http://localhost:9091", help="Pushgateway URL")
    parser.add_argument("--job", default="ecommerce_job", help="Pushgateway job name")
    parser.add_argument("--instance", default="ecommerce-sim-1", help="Instance label to push (grouping_key)")
    parser.add_argument("--interval", type=int, default=5, help="Seconds between pushes")
    args = parser.parse_args()

    simulate_and_push(args)

if __name__ == "__main__":
    main()
