# ☁️ Catálogo de Métricas de Observabilidad para Plataforma SaaS

Este catálogo documenta las métricas clave para monitorear el rendimiento, la estabilidad y el crecimiento de una aplicación SaaS moderna, enviadas usando `pushadd_to_gateway`.

Las métricas utilizan el prefijo `saas_` y están organizadas por dominio técnico/funcional.

## 1. ⏱ Rendimiento y Latencia (SLA/SLO)

Métricas que miden la velocidad y experiencia del usuario final.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `saas_active_sessions_gauge` | `gauge` | Sesiones de usuario activas concurrentes. | |
| `saas_api_latency_ms_gauge` | `gauge` | Latencia de API instantánea por endpoint. | `endpoint` |
| `saas_request_duration_seconds_histogram` | `histogram` | Distribución de la duración total de la solicitud (end-to-end). | |
| `saas_db_query_seconds_summary` | `summary` | Duración de consultas a la base de datos (con percentiles). | |
| `saas_cache_hit_ratio_gauge` | `gauge` | Porcentaje de aciertos de la caché. | `endpoint` |
| `saas_stream_bytes_total` | `counter` | Bytes totales procesados por servicios de streaming/colas. | |

## 2. 🚨 Errores y Estabilidad

Métricas de errores y disponibilidad del servicio.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `saas_api_requests_total_counter` | `counter` | Solicitudes totales a la API. | `endpoint`, `method`, `code` (HTTP status) |
| `saas_errors_total_counter` | `counter` | Errores internos de la aplicación (excepciones, lógica). | `endpoint` |
| `saas_error_rate_5m_gauge` | `gauge` | Tasa de errores aproximada sobre una ventana de 5 minutos (KPI derivado). | |

## 3. ⚙ Infraestructura y Operaciones (DevOps)

Métricas de la salud de los recursos de cómputo y las tareas asíncronas.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `saas_instance_cpu_percent_gauge` | `gauge` | Porcentaje de uso de CPU por instancia/contenedor. | `instance_id` |
| `saas_instance_memory_mb_gauge` | `gauge` | Uso de memoria (RAM) por instancia. | `instance_id` |
| `saas_db_connections_gauge` | `gauge` | Conexiones activas a la base de datos. | |
| `saas_deployments_total` | `counter` | Recuento de despliegues realizados. | |
| `saas_background_jobs_pending_gauge` | `gauge` | Tareas pendientes en las colas de procesamiento asíncrono. | |

## 4. 📈 Negocio y Flujo de Usuarios

Métricas relacionadas con el crecimiento, la activación y la configuración de la aplicación.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `saas_user_signup_total` | `counter` | Total de registros de nuevos usuarios. | |
| `saas_password_reset_total` | `counter` | Total de eventos de restablecimiento de contraseña. | |
| `saas_feature_flag_active_gauge` | `gauge` | Estado de un *feature flag* específico (0=Off, 1=On). | `flag` (ej. 'beta_ui') |

---

## 🛠 Ejecución y Configuración

El script `saas_push.py` utiliza `pushadd_to_gateway` para sumar las métricas de tipo `counter` e `histogram` en cada intervalo.

### Uso del Script

```bash
# Ejecutar la simulación cada 5 segundos
python3 business-case-5.py --pushgateway http://localhost:9091 --job saas_job --instance backend-app-01 --interval 5
```