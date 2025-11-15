# 🏥 Catálogo de Métricas de Observabilidad Hospitalaria

Este documento cataloga las métricas del sistema de gestión hospitalaria, diseñadas para ser enviadas de forma incremental mediante `pushadd_to_gateway` y monitoreadas con Prometheus.

Las métricas siguen la convención de prefijo `hospital_` y están segmentadas por áreas operacionales.

## 1. 🛌 Capacidad e Instalaciones

Métricas que miden la disponibilidad y el estado de los recursos físicos esenciales.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `hospital_beds_available_gauge` | `gauge` | Camas disponibles por pabellón. | `ward` (ej. 'General A', 'ICU') |
| `hospital_icu_occupancy_percent_gauge` | `gauge` | Porcentaje de ocupación de la Unidad de Cuidados Intensivos (ICU). | |
| `hospital_waiting_room_patients_gauge` | `gauge` | Número de pacientes esperando en la sala de emergencias. | |
| `hospital_ventilators_in_use_gauge` | `gauge` | Número de ventiladores mecánicos actualmente en uso. | |
| `hospital_isolation_rooms_available_gauge` | `gauge` | Habitaciones de aislamiento disponibles. | |
| `hospital_staff_on_duty_gauge` | `gauge` | Conteo de personal médico y de apoyo en turno. | |

## 2. 🚶 Flujo de Pacientes y Emergencia

Métricas que rastrean el movimiento de pacientes a través de la instalación y la demanda de emergencia.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `hospital_admissions_total` | `counter` | Total de ingresos hospitalarios. | |
| `hospital_discharges_total` | `counter` | Total de altas hospitalarias. | |
| `hospital_icu_admissions_total` | `counter` | Total de ingresos a la UCI. | |
| `hospital_emergency_calls_total` | `counter` | Llamadas de emergencia recibidas. | |
| `hospital_appointments_completed_total` | `counter` | Citas médicas completadas en clínicas. | `clinic` (ej. 'Cardiology') |
| `hospital_er_wait_time_minutes_histogram` | `histogram` | Distribución del tiempo de espera en la sala de emergencias (minutos). | |

## 3. ✨ Calidad y Seguridad Clínica

Métricas enfocadas en la calidad de la atención, eventos adversos y reingresos.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `hospital_medication_errors_total` | `counter` | Errores en la administración de medicamentos. | |
| `hospital_patient_readmissions_total` | `counter` | Reingresos de pacientes (ej. dentro de 30 días). | |
| `hospital_telemetry_errors_total` | `counter` | Errores en la monitorización remota o telemetría. | |
| `hospital_surgery_duration_minutes_summary` | `summary` | Duración de las cirugías (minutos), incluyendo percentiles. | |
| `hospital_cleanliness_score_gauge` | `gauge` | Puntuación promedio de limpieza/sanidad diaria. | |

## 4. 📦 Logística y Recursos

Métricas de inventario crítico.

| Métrica | Tipo | Descripción | Etiquetas Clave |
| :--- | :--- | :--- | :--- |
| `hospital_med_supplies_remaining_gauge` | `gauge` | Unidades restantes de suministros médicos clave. | `supply_type` (ej. 'Masks', 'Gloves') |

---

## 🛠 Ejecución y Configuración

El script `hospital_push.py` utiliza `pushadd_to_gateway` para sumar las métricas de tipo `counter` e `histogram` en cada intervalo.

### Uso del Script

```bash
# Ejecutar la simulación
python3 business-case-3.py --pushgateway http://localhost:9091 --job hospital_job --instance main-campus-sim --interval 5
```