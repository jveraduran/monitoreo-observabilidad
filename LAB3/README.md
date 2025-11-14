# 📘 README — Consultas PromQL y Proyecto de Observabilidad

Este documento contiene:

- Instalación del entorno (Docker, Prometheus, Pushgateway, Python)
- Arquitectura general
- Archivos del proyecto
- Consultas PromQL organizadas por:
  - Tipo de métrica
  - Categorías
  - Funciones
  - Operadores (con ejemplos completos)

---

# 🧩 Arquitectura General

```
[Python Script] → [Pushgateway] → [Prometheus Local] → [Grafana Cloud]
```

1. El script en Python envía métricas al **Pushgateway**.  
2. **Prometheus** obtiene estas métricas mediante `scrape_configs`.  
3. Luego Prometheus reenvía las métricas a **Grafana Cloud** vía `remote_write`.

---

# ✅ Prerrequisitos

- Servidor Debian o Ubuntu
- Docker + Docker Compose instalado
- Python 3.10+
- Librería `prometheus-client`
- Token de Grafana Cloud
- Acceso sudo

---

# 🐳 Instalación de Docker

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
```

Agregar clave GPG:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Agregar repositorio:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

Instalar:

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verificar:

```bash
sudo docker version
sudo docker info
```

---

# 🐍 Instalar Python + dependencias

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
```

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar librería Prometheus:

```bash
pip install prometheus_client
```

---

# 🛠️ Archivos del Proyecto

## 1️⃣ `docker-compose.yml`

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    volumes:
      - ./prom/config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    depends_on:
      - pushgateway
      - node-exporter
    networks:
      - prom-net

  pushgateway:
    image: prom/pushgateway:latest
    container_name: pushgateway
    ports:
      - "9091:9091"
    networks:
      - prom-net

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    ports:
      - "9100:9100"
    networks:
      - prom-net

networks:
  prom-net:
    driver: bridge

volumes:
  prometheus_data:
```

---

## 2️⃣ `prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "pushgateway"
    static_configs:
      - targets: ["pushgateway:9091"]

remote_write:
  - url: "<PROMETHEUS_URL>"
    basic_auth:
      username: "<GRAFANA_INSTANCE_ID>"
      password: "<GRAFANA_API_KEY>"
```

---

# 📡 Ejecutar Prometheus + Pushgateway

```bash
docker compose up -d
```

---

# 🐍 Ejecutar el script Python

```bash
python3 app.py
```

---

# 🔍 Revisar métricas

Prometheus local:

```
http://IP_PUBLICA:9090
```

Pushgateway:

```
http://IP_PUBLICA:9091
```

---

# 📊 1. Tipos de métricas y consultas PromQL

---

## 🟦 1. Gauge — valores que suben y bajan

Ejemplos: CPU, RAM, temperatura.

### 📚 Tabla de referencia oficial (Gauges)
| Item | Enlace |
|------|--------|
| Tipo de métrica Gauge | https://prometheus.io/docs/concepts/metric_types/#gauge |
| Range Vectors | https://prometheus.io/docs/prometheus/latest/querying/basics/#range-vector-selectors |
| Aggregations | https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators |

### Consultas:

```promql
app_temperature_celsius
avg(app_cpu_usage_percent)
min(app_temperature_celsius)
max(app_cpu_usage_percent)
app_cpu_usage_percent[5m]
```

---

## 🟧 2. Counter — métricas que solo incrementan

### 📚 Referencia oficial (Counters)
| Item | Enlace |
|------|--------|
| Tipo Counter | https://prometheus.io/docs/concepts/metric_types/#counter |
| rate() | https://prometheus.io/docs/prometheus/latest/querying/functions/#rate |
| increase() | https://prometheus.io/docs/prometheus/latest/querying/functions/#increase |

### Consultas típicas:

```promql
rate(app_requests_total[1m])
increase(app_errors_total[5m])
irate(app_requests_total[1m])
sum(rate(app_requests_total[5m])) by (job)
```

---

## 🟩 3. Summary — percentiles calculados en cliente

### 📚 Referencia oficial (Summary)
| Item | Enlace |
|------|--------|
| Summary | https://prometheus.io/docs/concepts/metric_types/#summary |

```promql
rate(app_processing_time_seconds_sum[5m]) / rate(app_processing_time_seconds_count[5m])
app_processing_time_seconds{quantile="0.9"}
```

---

## 🟪 4. Histogram — distribuciones y buckets

### 📚 Referencia oficial (Histogram)
| Item | Enlace |
|------|--------|
| Histogram | https://prometheus.io/docs/concepts/metric_types/#histogram |
| histogram_quantile() | https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile |

```promql
app_request_latency_seconds_bucket
rate(app_request_latency_seconds_bucket[5m])
histogram_quantile(
  0.95,
  sum(rate(app_request_latency_seconds_bucket[5m])) by (le)
)
```

---

# 🔥 2. Categorías de consultas PromQL

| Categoría | Descripción | Documentación |
|----------|-------------|---------------|
| Selección | Selección de series | https://prometheus.io/docs/prometheus/latest/querying/basics/ |
| Aritmética | Operaciones sobre series | https://prometheus.io/docs/prometheus/latest/querying/operators/#arithmetic-binary-operators |
| Comparación | Filtros comparativos | https://prometheus.io/docs/prometheus/latest/querying/operators/#comparison-operators |
| Lógicos | Relaciones entre series | https://prometheus.io/docs/prometheus/latest/querying/operators/#set-binary-operators |

## Selección simple

```promql
metric
metric{job="app"}
metric[5m]
```

## Aritmética

```promql
cpu_usage / 100
rate(app_requests_total[1m]) * 60
```

## Comparaciones

```promql
app_cpu_usage_percent > 80
```

## Agrupaciones

```promql
sum(app_cpu_usage_percent) by (instance)
```

## Funciones comunes

## Tabla completa de funciones oficiales usadas

| Función | Ejemplo | Documentación |
|---------|---------|----------------|
| rate() | rate(app_requests_total[5m]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#rate |
| irate() | irate(app_requests_total[1m]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#irate |
| increase() | increase(app_errors_total[1h]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#increase |
| delta() | delta(app_cpu_usage_percent[5m]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#delta |
| changes() | changes(app_temperature_celsius[15m]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#changes |
| resets() | resets(app_requests_total[1h]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#resets |
| deriv() | deriv(app_cpu_usage_percent[5m]) | https://prometheus.io/docs/prometheus/latest/querying/functions/#deriv |
| predict_linear() | predict_linear(app_cpu_usage_percent[5m], 600) | https://prometheus.io/docs/prometheus/latest/querying/functions/#predict_linear |
| histogram_quantile() | histogram_quantile(0.9, …) | https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile |
| label_join() | label_join(metric,"a","-","b","c") | https://prometheus.io/docs/prometheus/latest/querying/functions/#label_join |
| label_replace() | label_replace(metric,"a","$1","b","(.*)") | https://prometheus.io/docs/prometheus/latest/querying/functions/#label_replace |

```
rate(), irate(), increase(), delta(), changes(), resets(),
deriv(), predict_linear(), histogram_quantile(),
label_join(), label_replace()
```

## rate()
```
rate(app_requests_total[5m])
rate(app_errors_total[5m])
```

## irate()
```
irate(app_requests_total[1m])
```

## increase()
```
increase(app_requests_total[10m])
increase(app_errors_total[1h])
```

## delta()
```
delta(app_temperature_celsius[10m])
delta(app_cpu_usage_percent[5m])
```

## changes()
```
changes(app_temperature_celsius[15m])
```

## resets()
```
resets(app_requests_total[1h])
```

## deriv()
```
deriv(app_cpu_usage_percent[5m])
```

## predict_linear()
```
predict_linear(app_cpu_usage_percent[5m], 600)
```

## histogram_quantile()
```
histogram_quantile(0.5, rate(app_request_latency_seconds_bucket[5m]))
histogram_quantile(0.9, rate(app_request_latency_seconds_bucket[5m]))
histogram_quantile(0.99, rate(app_request_latency_seconds_bucket[5m]))
```

## label_join()
```
label_join(app_requests_total, "source", "-", "job", "instance")
```

## label_replace()
```
label_replace(app_requests_total, "job", "$1-demo", "job", "(.*)")
label_replace(app_requests_total, "host", "$1", "instance", "(.*):.*")
```

## Joins entre series

```promql
sum(rate(a[5m])) by (job) * on(job) group_left(version) build_info
```

---

# 🔥 3. Operadores en PromQL (con ejemplos)

## Tabla de operadores

| Tipo | Operadores | Documentación |
|------|-------------|---------------|
| Aritméticos | `+ - * / % ^` | https://prometheus.io/docs/prometheus/latest/querying/operators/#arithmetic-binary-operators |
| Comparación | `== != > < >= <=` | https://prometheus.io/docs/prometheus/latest/querying/operators/#comparison-operators |
| Lógicos | `and or unless` | https://prometheus.io/docs/prometheus/latest/querying/operators/#logical-set-binary-operators |
| Modificadores | `on() ignoring() group_left group_right` | https://prometheus.io/docs/prometheus/latest/querying/operators/#vector-matching |

## Aritméticos

```
+  -  *  /  %  ^
```

```promql
app_memory_free_mb + app_memory_used_mb
app_memory_total_mb - app_memory_free_mb
(app_cpu_usage_percent / 100) * app_cpu_cores
(app_requests_total % 10)
(app_cpu_usage_percent ^ 2)
```

## Comparación

```
==  !=  >  <  >=  <=
```

```promql
app_cpu_usage_percent > 80
app_errors_total >= 1
app_requests_total != 0
```

## Lógicos

```
and   or   unless
```

```promql
(app_cpu_usage_percent > 80) and (app_memory_free_mb < 500)
(app_errors_total > 0) or (app_request_latency_seconds > 1)
up == 0 unless on(instance) node_maintenance_mode == 1
```

## Modificadores

```
on(), ignoring(), group_left, group_right
```

```promql
rate(app_requests_total[5m]) / ignoring(instance) rate(app_capacity_total[5m])
sum(rate(app_requests_total[5m])) by (job) / on(job) group_left(version) app_build_info
```

---

# 📚 **Resumen Final — Todas las Referencias Oficiales**

| Categoría | Documento |
|-----------|-----------|
| Tipos de métricas | https://prometheus.io/docs/concepts/metric_types/ |
| Querying Basics | https://prometheus.io/docs/prometheus/latest/querying/basics/ |
| Operadores | https://prometheus.io/docs/prometheus/latest/querying/operators/ |
| Funciones | https://prometheus.io/docs/prometheus/latest/querying/functions/ |

# ⏱️ Tiempo estimado total

**1 hora completa**
