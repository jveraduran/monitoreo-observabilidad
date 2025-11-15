# 📡 Catálogo de Métricas de Observabilidad Telecom/ISP

Este catálogo documenta las métricas clave para monitorear la infraestructura y calidad de servicio (QoS) de un proveedor de internet/telecomunicaciones, enviadas usando `pushadd_to_gateway`.

Las métricas utilizan el prefijo `isp_` y están organizadas por dominio.

## 1. 👥 Clientes y Capacidad

Métricas que miden la carga de la red y la base de clientes activos.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `isp_active_customers_gauge` | `gauge` | Clientes conectados/activos. | `region` |
| `isp_peak_users_gauge` | `gauge` | Máximo de usuarios concurrentes en el último intervalo. | |
| `isp_current_bandwidth_mbps_gauge` | `gauge` | Uso total de ancho de banda (instante en Mbps). | |
| `isp_routers_online_gauge` | `gauge` | Conteo de routers de core/borde activos. | |
| `isp_reconnects_total` | `counter` | Eventos de reconexión forzada o de cliente (churn técnico). | |

## 2. 🌐 Red y Rendimiento (Tráfico)

Métricas fundamentales de la salud y el flujo de la red.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `isp_throughput_bytes_total` | `counter` | Total de bytes transferidos (tráfico acumulado). | |
| `isp_packets_dropped_total` | `counter` | Paquetes totales descartados/perdidos. | `router` |
| `isp_connection_errors_total` | `counter` | Errores de establecimiento de conexión. | `protocol` (ej. 'dhcp', 'pppoe') |
| `isp_bandwidth_usage_mbps_histogram` | `histogram` | Distribución del ancho de banda utilizado por usuarios/segmentos. | |

## 3. ⏱ Calidad de Servicio (QoS)

Métricas que miden la experiencia percibida por el usuario.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `isp_average_latency_ms_gauge` | `gauge` | Latencia promedio de la red (milisegundos). | `region` |
| `isp_avg_jitter_ms_gauge` | `gauge` | Jitter (variación de la latencia) promedio (milisegundos). | |
| `isp_latency_ms_histogram` | `histogram` | Distribución de los valores de latencia. | |
| `isp_outages_total` | `counter` | Interrupciones de servicio registradas. | `cause` (ej. 'power_loss', 'fiber_cut') |
| `isp_repair_time_hours_summary` | `summary` | Tiempo de reparación (MTTR) de interrupciones (horas). | |
| `isp_sla_violations_total` | `counter` | Incumplimientos del Acuerdo de Nivel de Servicio (SLA). | |
| `isp_customer_complaints_total` | `counter` | Quejas de clientes registradas. | `topic` (ej. 'speed', 'outage') |

---

## 🛠 Ejecución y Configuración

El script `telecom_push.py` debe ejecutarse de forma persistente y utiliza `pushadd_to_gateway` para sumar los contadores y las distribuciones en cada intervalo.

### Uso del Script

```bash
# Ejecutar la simulación cada 5 segundos
python3 business-case-4.py --pushgateway http://localhost:9091 --job telecom_job --instance core-sim-us-east --interval 5
```