from flask import Flask, Response
from prometheus_client import CollectorRegistry, Gauge, generate_latest
import random

app = Flask(__name__)
registry = CollectorRegistry()

# Métricas custom
temperature = Gauge('app_temperature_celsius', 'Temperatura del sistema', registry=registry)
cpu_usage = Gauge('app_cpu_usage_percent', 'Uso de CPU', registry=registry)

@app.route('/metrics')
def metrics():
    temperature.set(random.uniform(20.0, 35.0))
    cpu_usage.set(random.uniform(0, 100))
    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)