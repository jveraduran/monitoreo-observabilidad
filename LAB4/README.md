# 📘 README --- Consultas PromQL y Proyecto de Observabilidad

Este documento contiene:

-   Instalación del entorno (Docker, Prometheus, Pushgateway, Python)
-   Arquitectura general
-   Archivos del proyecto
-   Consultas PromQL organizadas por:
    -   Tipo de métrica
    -   Categorías
    -   Funciones
    -   Operadores (con ejemplos completos)
-   **Actividad final del laboratorio: construcción de dashboard en
    Grafana Cloud**

------------------------------------------------------------------------

# 🧩 Arquitectura General

    [Python Script] → [Pushgateway] → [Prometheus Local] → [Grafana Cloud]

1.  El script en Python envía métricas al **Pushgateway**.\
2.  **Prometheus** obtiene estas métricas mediante `scrape_configs`.\
3.  Prometheus reenvía las métricas a **Grafana Cloud** mediante
    `remote_write`.

------------------------------------------------------------------------

# ✅ Prerrequisitos

-   Servidor Debian o Ubuntu\
-   Docker + Docker Compose instalado\
-   Python 3.10+\
-   Librería `prometheus-client`\
-   Token de Grafana Cloud\
-   Acceso sudo

------------------------------------------------------------------------

# 🐳 Instalación de Docker

``` bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release
```

Agregar clave GPG:

``` bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Agregar repositorio:

``` bash
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg]   https://download.docker.com/linux/debian   $(lsb_release -cs) stable"   | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
```

Instalar:

``` bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verificar:

``` bash
sudo docker version
sudo docker info
```

------------------------------------------------------------------------

# 🐍 Instalar Python + dependencias

``` bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
```

Crear entorno virtual:

``` bash
python3 -m venv venv
source venv/bin/activate
```

Instalar librería Prometheus:

``` bash
pip install prometheus_client requests
```

Clonar repositorio:

``` bash
git clone https://github.com/jveraduran/monitoreo-observabilidad.git
```

Ingresar a la carpeta del laboratorio:

``` bash
cd monitoreo-observabilidad/LAB4
```

------------------------------------------------------------------------

# 🛠️ Archivos del Proyecto

## 1️⃣ `docker-compose.yml`

``` yaml
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

------------------------------------------------------------------------

## 2️⃣ `prometheus.yml`

``` yaml
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

------------------------------------------------------------------------

# 📡 Ejecutar Prometheus + Pushgateway

``` bash
sudo docker compose up -d
sudo docker ps
```

Si Prometheus muestra error de permisos en el directorio de datos:

``` bash
sudo rm -rf data
sudo mkdir data
sudo chown -R 65534:65534 data
sudo chmod -R 775 data
```

Reiniciar:

``` bash
sudo docker compose down
sudo docker compose up -d
```

------------------------------------------------------------------------

# 🐍 Ejecutar el script Python

``` bash
python3 business-case-[X].py
```

Documentación oficial en [Python Client](https://prometheus.github.io/client_python/)

------------------------------------------------------------------------

# 🔍 Revisar métricas

Prometheus local:

    http://IP_PUBLICA:9090

Pushgateway:

    http://IP_PUBLICA:9091

------------------------------------------------------------------------

# 🧪 Actividad Final del Laboratorio

Al finalizar la instalación y ejecución de métricas, cada estudiante
deberá:

## ✅ 1. Elegir uno de los siguientes *business cases*:

-   business-case-1.py
-   business-case-2.py
-   business-case-3.py
-   business-case-4.py
-   business-case-5.py

Cada caso contiene un conjunto distinto de métricas y escenarios
operacionales.

------------------------------------------------------------------------

## ✅ 2. Construir un Dashboard en Grafana Cloud

El dashboard debe incluir:

### ✔️ Al menos **8 visualizaciones**

### ✔️ Deben tener **sentido operacional**

### ✔️ Deben basarse en consultas PromQL reales

------------------------------------------------------------------------

# ⏱️ Tiempo estimado total

**1 hora completa**
