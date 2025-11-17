import time
import random
import argparse
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, push_to_gateway

registry = CollectorRegistry()

# Métricas de Negocio
ECOM_REVENUE_TOTAL = Counter('ecom_revenue_total', 'Total revenue generated.', ['job', 'instance', 'region', 'gateway'], registry=registry)
ECOM_ORDERS_PAID_TOTAL = Counter('ecom_orders_paid_total', 'Total number of paid orders.', ['job', 'instance', 'region'], registry=registry)
ECOM_CART_CREATED_TOTAL = Counter('ecom_cart_created_total', 'Total number of carts created.', ['job', 'instance', 'region'], registry=registry)
FUNNEL_STEP_TOTAL = Counter('funnel_step_total', 'Count of users reaching a funnel step.', ['job', 'instance', 'region', 'step'], registry=registry)
PAYMENT_REQUEST_TOTAL = Counter('payment_request_total', 'Total payment requests.', ['job', 'instance'], registry=registry)
PAYMENT_SUCCESS_TOTAL = Counter('payment_success_total', 'Total successful payments.', ['job', 'instance', 'gateway'], registry=registry)

SHIPPING_TIME_SECONDS = Histogram(
    'shipping_time_seconds', 
    'Time from dispatch to customer delivery.', 
    ['job', 'instance', 'region'], 
    buckets=[3600, 10800, 21600, 43200, 86400, 172800, 345600], # 1h, 3h, 6h, 12h, 1d, 2d, 4d
    registry=registry
)
PAYMENT_REFUND_TOTAL = Counter('payment_refund_total', 'Total number of refunds processed.', ['job', 'instance'], registry=registry)
SHIPPING_ORDER_RETURNED_TOTAL = Counter('shipping_order_returned_total', 'Total number of orders returned.', ['job', 'instance', 'region'], registry=registry)

# Métricas de Errores y Latencia (Backend)
API_REQUESTS_TOTAL = Counter('api_requests_total', 'Total count of API requests.', ['job', 'instance', 'service'], registry=registry)
API_ERRORS_TOTAL = Counter('api_errors_total', 'Total count of API errors by HTTP code.', ['job', 'instance', 'service', 'code'], registry=registry)
API_LATENCY_SECONDS = Histogram('api_latency_seconds', 'API request latency.', ['job', 'instance', 'service'], registry=registry)

# Métricas de Infraestructura y Colas
QUEUE_PROCESSING_SIZE = Gauge('queue_processing_size', 'Current size of the processing queue.', ['job', 'instance', 'queue'], registry=registry)
DB_QUERY_TIME_SECONDS = Histogram(
    'db_query_time_seconds', 
    'Database query execution latency.', 
    ['job', 'instance'], 
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0], 
    registry=registry
)

CACHE_HIT_RATIO = Gauge('cache_hit_ratio', 'Ratio of cache hits to total requests.', ['job', 'instance', 'cache_name'], registry=registry)
DB_CONNECTIONS_ACTIVE = Gauge('db_connections_active', 'Number of active database connections.', ['job', 'instance', 'pool'], registry=registry)

# Métricas de Frontend (UX)
FRONTEND_PAGE_LOAD_SECONDS = Histogram(
    'frontend_page_load_seconds', 
    'Time taken to load the page.', 
    ['job', 'instance'], 
    buckets=[0.5, 1.0, 2.5, 5.0, 10.0], 
    registry=registry
)
FRONTEND_JS_ERRORS_TOTAL = Counter(
    'frontend_js_errors_total', 
    'Total count of JavaScript errors detected.', 
    ['job', 'instance'], 
    registry=registry
)

# Métricas de INFRAESTRUCTURA (HOST)
CPU_USAGE_PERCENT = Gauge('cpu_usage_percent', 'Current CPU usage percentage.', ['job', 'instance'], registry=registry)
MEMORY_USAGE_BYTES = Gauge('memory_usage_bytes', 'Current memory usage in bytes.', ['job', 'instance'], registry=registry)

# Constantes
REGIONS = ['US-East', 'EU-West', 'APAC']
SERVICES = ['orders', 'checkout', 'products', 'users']
GATEWAYS = ['stripe', 'paypal', 'adp']

# --- 2. LÓGICA DE SIMULACIÓN ---

def simulate_ecommerce_traffic(job_name, instance_name):
    # Lógica de Negocio, Backend, Frontend e Infraestructura (Mantiene la lógica anterior)
    
    # ... (Código previo omitido por brevedad, asumiendo que incluye todas las métricas anteriores)
    
    for region in REGIONS:
        ECOM_CART_CREATED_TOTAL.labels(job=job_name, instance=instance_name, region=region).inc(random.randint(100, 200))
        FUNNEL_STEP_TOTAL.labels(job=job_name, instance=instance_name, region=region, step='cart_created').inc(random.randint(100, 200))
        checkouts = random.randint(30, 80)
        FUNNEL_STEP_TOTAL.labels(job=job_name, instance=instance_name, region=region, step='checkout_start').inc(checkouts)
        orders_paid = random.randint(int(checkouts * 0.3), int(checkouts * 0.7))
        ECOM_ORDERS_PAID_TOTAL.labels(job=job_name, instance=instance_name, region=region).inc(orders_paid)
        FUNNEL_STEP_TOTAL.labels(job=job_name, instance=instance_name, region=region, step='order_paid').inc(orders_paid)
        revenue = orders_paid * random.uniform(20.0, 150.0) 
        
        for gateway in GATEWAYS:
            rev_share = revenue * 0.6 if gateway == 'stripe' else revenue * 0.2
            ECOM_REVENUE_TOTAL.labels(job=job_name, instance=instance_name, region=region, gateway=gateway).inc(rev_share * 100)
            PAYMENT_SUCCESS_TOTAL.labels(job=job_name, instance=instance_name, gateway=gateway).inc(rev_share / 50)
            PAYMENT_REQUEST_TOTAL.labels(job=job_name, instance=instance_name).inc(rev_share / 50 + random.randint(0, 2))

    for service in SERVICES:
        requests = random.randint(500, 1000)
        API_REQUESTS_TOTAL.labels(job=job_name, instance=instance_name, service=service).inc(requests)
        
        for _ in range(requests):
            API_LATENCY_SECONDS.labels(job=job_name, instance=instance_name, service=service).observe(random.uniform(0.05, 0.4))
            
        errors_500 = int(requests * 0.02)
        if errors_500 > 0:
            API_ERRORS_TOTAL.labels(job=job_name, instance=instance_name, service=service, code='500').inc(errors_500)

        errors_503 = int(requests * 0.005)
        if errors_503 > 0:
            API_ERRORS_TOTAL.labels(job=job_name, instance=instance_name, service=service, code='503').inc(errors_503)

    db_queries = random.randint(100, 300)
    for _ in range(db_queries):
        DB_QUERY_TIME_SECONDS.labels(job=job_name, instance=instance_name).observe(random.uniform(0.005, 0.15))
    
    QUEUE_PROCESSING_SIZE.labels(job=job_name, instance=instance_name, queue='orders').set(random.randint(0, 150))
    QUEUE_PROCESSING_SIZE.labels(job=job_name, instance=instance_name, queue='shipment').set(random.randint(0, 50))

    page_loads = random.randint(400, 600)
    for _ in range(page_loads):
        FRONTEND_PAGE_LOAD_SECONDS.labels(job=job_name, instance=instance_name).observe(random.uniform(0.8, 4.0)) 
    
    js_errors = random.randint(1, 5) 
    FRONTEND_JS_ERRORS_TOTAL.labels(job=job_name, instance=instance_name).inc(js_errors)

    CPU_USAGE_PERCENT.labels(job=job_name, instance=instance_name).set(random.uniform(10.0, 75.0))
    MEMORY_USAGE_BYTES.labels(job=job_name, instance=instance_name).set(random.randint(500000000, 2000000000))


    # 1. Logística y Devoluciones
    for region in REGIONS:
        # Simula el tiempo de envío (segundos)
        SHIP_TIME = random.uniform(86400, 259200) # Entre 1 día (86400s) y 3 días
        SHIPPING_TIME_SECONDS.labels(job=job_name, instance=instance_name, region=region).observe(SHIP_TIME)
        
        # Simula devoluciones (counter)
        returns = random.randint(1, 5)
        SHIPPING_ORDER_RETURNED_TOTAL.labels(job=job_name, instance=instance_name, region=region).inc(returns)
        
    # 2. Reembolsos (counter)
    refunds = random.randint(1, 10)
    PAYMENT_REFUND_TOTAL.labels(job=job_name, instance=instance_name).inc(refunds)

    # 3. Cache Hit Ratio (Gauge)
    # Cache de productos (90%-99%)
    CACHE_HIT_RATIO.labels(job=job_name, instance=instance_name, cache_name="products").set(random.uniform(0.90, 0.99))
    # Cache de usuarios (70%-85%)
    CACHE_HIT_RATIO.labels(job=job_name, instance=instance_name, cache_name="users").set(random.uniform(0.70, 0.85))

    # 4. Conexiones DB Activas (Gauge)
    # Pool principal de conexiones
    DB_CONNECTIONS_ACTIVE.labels(job=job_name, instance=instance_name, pool="main").set(random.randint(10, 50))
    # Pool de reportes
    DB_CONNECTIONS_ACTIVE.labels(job=job_name, instance=instance_name, pool="reports").set(random.randint(1, 5))


# --- 3. FUNCIÓN PRINCIPAL Y PARSING DE ARGUMENTOS ---

def main():
    parser = argparse.ArgumentParser(description="Simulador de métricas E-commerce y Pushgateway.")
    parser.add_argument('--pushgateway', type=str, required=True, help='URL y puerto del Pushgateway (ej: http://192.168.1.10:9091)')
    parser.add_argument('--job', type=str, required=True, help='Nombre del job de Prometheus (ej: ecommerce_job)')
    parser.add_argument('--instance', type=str, required=True, help='Nombre de la instancia (ej: ecommerce-sim-1)')
    parser.add_argument('--interval', type=int, default=10, help='Intervalo de push en segundos.')
    args = parser.parse_args()

    pushgateway_url = args.pushgateway
    job_name = args.job
    instance_name = args.instance
    interval = args.interval

    print(f"🚀 Iniciando simulación para Job: {job_name}, Instance: {instance_name}")
    print(f"🔗 Pushgateway: {pushgateway_url} (Intervalo: {interval}s)")

    while True:
        try:
            simulate_ecommerce_traffic(job_name, instance_name)
            
            grouping_key = {'instance': instance_name}

            push_to_gateway(
                pushgateway_url,
                job=job_name, 
                registry=registry, 
                grouping_key=grouping_key
            )
            print(f"✅ [{time.strftime('%H:%M:%S')}] Métricas enviadas correctamente al Pushgateway.")
            
        except Exception as e:
            print(f"❌ Error al enviar métricas: {e}")

        time.sleep(interval)


if __name__ == '__main__':
    main()