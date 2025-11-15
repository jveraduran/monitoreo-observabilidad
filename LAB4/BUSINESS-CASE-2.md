# 🏦 Catálogo de Métricas Clave del Core Bancario (Prometheus / Pushadd)

Este documento cataloga las métricas utilizadas en la simulación de observabilidad bancaria, enviadas de forma incremental mediante `pushadd_to_gateway`.

## 1. 💳 Transacciones y Negocio Central

Métricas de la salud transaccional y nuevos clientes.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `bank_transaction_total` | `counter` | Total de transacciones procesadas (transferencias, pagos, etc.). | `type`, `status`, `channel` |
| `bank_transaction_value_total` | `counter` | Valor monetario total procesado. | `type` |
| `bank_new_accounts_total` | `counter` | Apertura de nuevas cuentas. | `product` (ej. 'checking', 'savings') |
| `bank_payments_processing_time_seconds` | `histogram` | Latencia de procesamiento de pagos interbancarios (worker). | |

## 2. 💰 Originación de Crédito y Riesgo

Métricas del flujo de crédito y riesgo financiero.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `credit_application_total` | `counter` | Total de solicitudes de crédito recibidas. | `product_type` |
| `credit_application_approved_total` | `counter` | Solicitudes aprobadas. | `product_type` |
| `credit_application_latency_seconds` | `histogram` | Tiempo total de procesamiento (solicitud → decisión). | |
| `bank_npl_ratio` | `gauge` | **Ratio de Préstamos No Productivos (NPL)**. | |

## 3. 🏧 Cajeros Automáticos (ATM) y Red Física

Métricas operacionales de la red de cajeros y terminales.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `atm_transaction_total` | `counter` | Transacciones totales en ATMs. | `operation` (ej. 'withdrawal', 'deposit') |
| `atm_out_of_service_total` | `counter` | Eventos de cajeros fuera de servicio. | `reason` (ej. 'no_cash', 'hardware_fail') |
| `atm_device_status` | `gauge` | **Estado binario del dispositivo (1=activo, 0=inactivo)**. | `device_id` |
| `atm_cash_level_percent` | `gauge` | Nivel de efectivo restante. | `device_id` |

## 4. 🔐 Seguridad y Fraude

Métricas de acceso y detección de fraude.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `security_login_success_total` | `counter` | Inicios de sesión exitosos. | `channel` |
| `security_login_failed_total` | `counter` | Intentos de login fallidos. | `reason` (ej. 'credentials_fail') |
| `security_fraud_alerts_total` | `counter` | Alertas generadas por el sistema de fraude. | `severity` (ej. 'critical', 'high') |

## 5. ⚙ Backend y APIs

Métricas de rendimiento de los microservicios y la base de datos.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `api_requests_total` | `counter` | Total de requests a APIs del core bancario. | `service`, `code` (HTTP status) |
| `api_latency_seconds` | `histogram` | Latencia del procesamiento de requests por servicio. | `service` |
| `db_query_time_seconds` | `histogram` | Latencia de consultas a la base de datos. | |

---

## 🛠 Ejecución y Configuración

El script está diseñado para ejecutarse continuamente y usar `pushadd_to_gateway` para sumar los nuevos valores de los contadores e histogramas.

### Uso del Script

```bash
python3 business-case-2.py --pushgateway http://localhost:9091 --job banking_core_job --instance bank-prod-sim --interval 5
```