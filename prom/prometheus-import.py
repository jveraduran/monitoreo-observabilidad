from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import random, time

# Dirección del Pushgateway local
PUSHGATEWAY_URL = "http://localhost:9091"

# Registramos un conjunto de métricas (registry)
registry = CollectorRegistry()

# Definimos una métrica de ejemplo tipo Gauge (valor numérico variable)
temperature = Gauge('app_temperature_celsius', 'Temperatura del sistema', registry=registry)
cpu_usage = Gauge('app_cpu_usage_percent', 'Uso de CPU', registry=registry)

# Simulamos enviar métricas en un loop
while True:
    temperature.set(random.uniform(20.0, 35.0))
    cpu_usage.set(random.uniform(0, 100))
    push_to_gateway(PUSHGATEWAY_URL, job='python_demo_app', registry=registry)
    print("📤 Métricas enviadas al Pushgateway")
    time.sleep(15)
