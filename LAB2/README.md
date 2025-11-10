# Laboratorio de Observabilidad con Alloy, Prometheus y Blackbox Exporter

Este laboratorio muestra cómo implementar observabilidad en un servidor Debian usando **Alloy**, **Prometheus exporters** (cAdvisor y Blackbox) y métricas custom de Python/Flask. Incluye instalación, configuración, validación y consultas de métricas.

---

## 1️⃣ Prerrequisitos

* Servidor Debian (local o nube)
* Acceso root o sudo
* Token de Grafana Cloud (`GCLOUD_RW_API_KEY`) para remote_write

---

## 2️⃣ Instalación de Docker

1. **Actualizar sistema**

```bash
sudo apt update && sudo apt upgrade -y
```

2. **Instalar dependencias necesarias**

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

3. **Agregar clave GPG de Docker**

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

4. **Agregar repositorio oficial de Docker**

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

5. **Instalar Docker y componentes**

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

6. **Verificar instalación**

```bash
sudo docker version
sudo docker info
```

---

## 3️⃣ Instalación de Alloy

Reemplaza `[TOKEN]` con tu API Key de Grafana Cloud.

```bash
GCLOUD_HOSTED_METRICS_ID="2732615" \
GCLOUD_HOSTED_METRICS_URL="https://prometheus-prod-56-prod-us-east-2.grafana.net/api/push" \
GCLOUD_HOSTED_LOGS_ID="1361984" \
GCLOUD_HOSTED_LOGS_URL="https://logs-prod-036.grafana.net/loki/api/v1/push" \
GCLOUD_FM_URL="https://fleet-management-prod-008.grafana.net" \
GCLOUD_FM_POLL_FREQUENCY="60s" \
GCLOUD_FM_HOSTED_ID="1404190" \
ARCH="amd64" \
GCLOUD_RW_API_KEY="[TOKEN]" \
/bin/sh -c "$(curl -fsSL https://storage.googleapis.com/cloud-onboarding/alloy/scripts/install-linux.sh)"
```

---

## 4️⃣ Configuración de Docker Compose

Crea un archivo `docker-compose.yml`:

```yaml
version: "3.8"

services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true

  blackbox_exporter:
    image: prom/blackbox-exporter:latest
    container_name: blackbox_exporter
    restart: unless-stopped
    ports:
      - "9115:9115"
    volumes:
      - ./blackbox.yml:/etc/blackbox_exporter/config.yml:ro
```

Crea el archivo `blackbox.yml`:

```yaml
modules:
  http_2xx:
    prober: http
    timeout: 5s
    http:
      method: GET

  tcp_connect:
    prober: tcp
    timeout: 5s

  icmp:
    prober: icmp
    timeout: 5s
```

---

## 5️⃣ Configuración de Alloy `/etc/alloy/config.alloy`

Agrega los siguientes bloques al final de tu archivo /etc/alloy/config.alloy

```hcl
# Extra Exporters (cAdvisor)
prometheus.scrape "extra_exporters" {
  targets = [
    {
      __address__ = "localhost:8080",
    },
  ]
  scrape_interval = "15s"
  forward_to = [prometheus.remote_write.metrics_service.receiver]
}

# Blackbox Exporter
prometheus.scrape "blackbox_http_probe" {
  targets = [
    {
      __address__    = "localhost:9115",
      __param_target = "http://localhost:8080/metrics",
      instance       = "mi_ec2_app",
    },
  ]

  metrics_path = "/probe"

  params = {
    module = ["http_2xx"],
  }

  scrape_interval = "30s"
  forward_to      = [prometheus.remote_write.metrics_service.receiver]
}

# Python app custom metrics
prometheus.scrape "python_app_metrics" {
  targets = [
    {
      __address__ = "localhost:8081",
      instance    = "python_app",
    },
  ]

  metrics_path    = "/metrics"
  scrape_interval = "15s"
  forward_to      = [prometheus.remote_write.metrics_service.receiver]
}
```

---

## 6️⃣ Validar y reiniciar Alloy

```bash
/usr/bin/alloy validate /etc/alloy/config.alloy
sudo systemctl restart alloy
sudo systemctl status alloy
```

---

## 7️⃣ Verificar servicios corriendo

```bash
# cAdvisor
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/metrics
```
# Blackbox Exporter
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:9115/metrics
```
---

## 8️⃣ Métricas de cAdvisor

| Métrica     | Query                                                                         | Qué mide                             |
| ----------- | ----------------------------------------------------------------------------- | ------------------------------------ |
| CPU         | `rate(container_cpu_usage_seconds_total{instance="localhost:8080"}[5m])`      | Promedio de CPU usado por contenedor |
| Memoria     | `container_memory_usage_bytes{instance="localhost:8080"}`                     | Memoria usada en bytes               |
| Red entrada | `rate(container_network_receive_bytes_total{instance="localhost:8080"}[5m])`  | Bytes recibidos por segundo          |
| Red salida  | `rate(container_network_transmit_bytes_total{instance="localhost:8080"}[5m])` | Bytes enviados por segundo           |
| Disco       | `container_fs_usage_bytes{instance="localhost:8080"}`                         | Uso de filesystem en bytes           |

---

## 9️⃣ Métricas de Blackbox Exporter

| Métrica                                                | Qué mide                           |
| ------------------------------------------------------ | ---------------------------------- |
| `probe_success{instance="mi_ec2_app"}`                 | 1 = OK, 0 = fallo                  |
| `probe_duration_seconds{instance="mi_ec2_app"}`        | Latencia total del chequeo         |
| `probe_http_content_length{instance="mi_ec2_app"}`     | Tamaño del contenido HTTP recibido |
| `probe_dns_lookup_time_seconds{instance="mi_ec2_app"}` | Latencia DNS                       |
| `probe_http_status_code{instance="mi_ec2_app"}`        | Código HTTP de respuesta           |

---

## 1️⃣0️⃣ Métricas custom Python/Flask

1. Instalar Python en Debian:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
```

2. Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar librerías necesarias:

```bash
pip install prometheus_client flask
```

4. Crear archivo `app.py`:

```python
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
```

5. Ejecutar la aplicación:

```bash
python3 app.py
```

6. Verificar métricas:

```bash
curl http://localhost:8081/metrics
```

---

## 1️⃣1️⃣ Observaciones

* Alloy recolecta métricas locales y las envía a Grafana Cloud.
* Blackbox Exporter permite monitorear disponibilidad y latencia de endpoints.
* Python/Flask permite generar métricas custom para tus aplicaciones.

---

Este laboratorio documenta la instalación y configuración completa de **Alloy**, **Docker exporters** y **métricas custom**.
