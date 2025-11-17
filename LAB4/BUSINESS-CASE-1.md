# 📈 Catálogo de Métricas de Observabilidad para E-commerce

Este documento cataloga las métricas clave del sistema de e-commerce, organizadas por dominio de negocio y técnico. Estas métricas son fundamentales para el monitoreo, la alerta y el cálculo de KPIs (Key Performance Indicators).

## 1. 🛒 Ventas y Revenue (Negocio)

Métricas centradas en el desempeño comercial y el ciclo de la orden.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `ecom_orders_total` | `counter` | Total de órdenes creadas. |
| `ecom_orders_paid_total` | `counter` | Órdenes pagadas exitosamente. |
| `ecom_orders_failed_total` | `counter` | Órdenes fallidas (intentó pagar pero falló). |
| `ecom_revenue_total` | `counter` | Monto total pagado (normalizar en USD/CLP). |
| `ecom_cart_created_total` | `counter` | Carritos creados. |
| `ecom_cart_abandoned_total` | `counter` | Carritos abandonados. |
| `ecom_cart_conversion_ratio` | `gauge` | (Órdenes / carritos) en tiempo real. |
| `ecom_avg_order_value` | `gauge` | Revenue / Órdenes pagadas en ventana de tiempo. |
| `ecom_items_sold_total` | `counter` | Total de ítems vendidos. |
| `ecom_discount_usage_total` | `counter` | Número de descuentos aplicados. |

## 2. 💳 Pagos y Pasarelas (Payments)

Métricas enfocadas en la interacción con las pasarelas de pago.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `payment_request_total` | `counter` | Intentos de pago. |
| `payment_success_total` | `counter` | Pagos completados. |
| `payment_failed_total` | `counter` | Pagos rechazados por gateway. |
| `payment_timeout_total` | `counter` | Pagos que no recibieron respuesta. |
| `payment_processing_latency_seconds` | `histogram` | Latencia en el procesamiento de pagos. |
| `payment_refund_total` | `counter` | Reembolsos ejecutados. |

## 3. 🔄 Checkout y Funnel

Métricas para el seguimiento del flujo de conversión del usuario.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `funnel_step_view_total{step="product"}` | `counter` | Vistas de producto. |
| `funnel_step_view_total{step="cart"}` | `counter` | Carrito abierto. |
| `funnel_step_view_total{step="checkout"}` | `counter` | Checkout iniciado. |
| `funnel_step_view_total{step="address"}` | `counter` | Dirección completada. |
| `funnel_step_view_total{step="payment"}` | `counter` | Etapa de pago. |
| `funnel_step_conversion_ratio` | `gauge` | Ratio de conversión entre pasos. |

## 4. 📦 Logística, Despachos y Delivery

Métricas relacionadas con la gestión del inventario y la entrega de productos.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `shipping_order_dispatched_total` | `counter` | Órdenes despachadas. |
| `shipping_order_delivered_total` | `counter` | Órdenes entregadas exitosamente. |
| `shipping_order_returned_total` | `counter` | Órdenes devueltas / rechazos. |
| `shipping_cost_total` | `counter` | Gastos de envío totales. |
| `shipping_time_seconds` | `histogram` | Tiempo desde despacho → entrega. |
| `warehouse_inventory{product="X"}` | `gauge` | Stock actual por producto. |

## 5. ⚙ Backend: Microservicios y APIs

Métricas de rendimiento y salud de los servicios de backend.

### Tráfico API

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `api_requests_total{service="orders"}` | `counter` | Requests totales por servicio. |
| `api_errors_total{service="orders"}` | `counter` | Errores 4xx/5xx por servicio. |
| `api_latency_seconds{service="checkout"}` | `histogram` | Latencia de cada endpoint por servicio. |
| `api_active_sessions` | `gauge` | Usuarios activos. |

### Cuellos de botella

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `queue_processing_size{queue="orders"}` | `gauge` | Tamaño de la cola de órdenes. |
| `queue_processing_latency_seconds` | `histogram` | Latencia del worker al procesar cola. |
| `db_query_time_seconds` | `histogram` | Latencia de consultas a la base de datos. |
| `db_connections_active` | `gauge` | Conexiones actuales a la base de datos. |

## 6. 🖥 Front-end / UX

Métricas de la experiencia del usuario y rendimiento del lado del cliente.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `frontend_page_load_seconds` | `histogram` | TTFB / Page Load. |
| `frontend_js_errors_total` | `counter` | Errores de JavaScript. |
| `frontend_checkout_error_total` | `counter` | Errores de interfaz en el checkout. |

## 7. 🔐 Seguridad y Fraude

Métricas relacionadas con el acceso y la detección de actividades sospechosas.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `fraud_score_events_total` | `counter` | Eventos con score de fraude arriba de cierto límite. |
| `login_failed_total` | `counter` | Intentos fallidos de login. |
| `login_success_total` | `counter` | Logins exitosos. |
| `blocked_ip_total` | `counter` | IPs bloqueadas. |

## 8. 🧩 Infraestructura (DevOps/SRE)

Métricas esenciales para el estado y la capacidad de la infraestructura.

| Métrica | Tipo | Descripción |
| :--- | :--- | :--- |
| `cpu_usage_percent{instance}` | `gauge` | Uso de CPU en porcentaje. |
| `memory_usage_bytes{instance}` | `gauge` | Uso de RAM en bytes. |
| `fs_free_bytes{instance}` | `gauge` | Espacio libre en disco. |
| `pod_restarts_total{pod}` | `counter` | Reinicios de contenedores (pods). |
| `http_request_total{code="500"}` | `counter` | Errores importantes de servidor (ej. 500). |

---

# 🧠 KPIs de Negocio (PromQL)

Los siguientes KPIs se calculan utilizando las métricas base y la sintaxis de PromQL (Prometheus Query Language).

### Conversion Rate (Tasa de Conversión)

**Descripción:** Mide la eficiencia con la que los carritos creados se convierten en órdenes pagadas.

$$
\text{Conversion Rate} = \frac{\sum(\text{Órdenes Pagadas})}{\sum(\text{Carritos Creados})}
$$

**PromQL:**
```promql
sum(rate(ecom_orders_paid_total[15m]))
/ sum(rate(ecom_cart_created_total[15m]))
```

### Uso del Script

```bash
python3 business-case-1.py --pushgateway http://localhost:9091 --job ecommerce_job --instance ecommerce-sim-1 --interval 5
```