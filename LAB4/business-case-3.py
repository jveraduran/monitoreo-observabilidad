#!/usr/bin/env python3
"""
Hospital metrics simulator - Structured metric names (style B)
Generates 22+ metrics and pushes to Pushgateway job=hospital_job
"""
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# Gauges
hospital_beds_available_gauge = Gauge("hospital_beds_available_gauge", "Beds available by ward", ["ward"], registry=registry)
hospital_waiting_room_patients_gauge = Gauge("hospital_waiting_room_patients_gauge", "Patients waiting in ER", registry=registry)
hospital_icu_occupancy_percent_gauge = Gauge("hospital_icu_occupancy_percent_gauge", "ICU occupancy percent", registry=registry)

# Counters
hospital_appointments_completed_total = Counter("hospital_appointments_completed_total", "Appointments completed", registry=registry)
hospital_medication_errors_total = Counter("hospital_medication_errors_total", "Medication errors", registry=registry)
hospital_admissions_total = Counter("hospital_admissions_total", "Admissions total", registry=registry)
hospital_discharges_total = Counter("hospital_discharges_total", "Discharges total", registry=registry)

# Histograms
hospital_er_wait_time_minutes_histogram = Histogram(
    "hospital_er_wait_time_minutes_histogram",
    "ER wait time minutes distribution",
    buckets=[5,10,20,30,45,60,120],
    registry=registry
)

# Summaries
hospital_surgery_duration_minutes_summary = Summary("hospital_surgery_duration_minutes_summary", "Surgery durations minutes", registry=registry)

# Extra metrics
hospital_ventilators_in_use_gauge = Gauge("hospital_ventilators_in_use_gauge", "Ventilators in use", registry=registry)
hospital_med_supplies_remaining_gauge = Gauge("hospital_med_supplies_remaining_gauge", "Medical supplies remaining", registry=registry)
hospital_emergency_calls_total = Counter("hospital_emergency_calls_total", "Emergency calls", registry=registry)
hospital_staff_on_duty_gauge = Gauge("hospital_staff_on_duty_gauge", "Staff on duty count", registry=registry)
hospital_isolation_rooms_available_gauge = Gauge("hospital_isolation_rooms_available_gauge", "Isolation rooms available", registry=registry)
hospital_icu_admissions_total = Counter("hospital_icu_admissions_total", "ICU admissions total", registry=registry)
hospital_telemetry_errors_total = Counter("hospital_telemetry_errors_total", "Telemetry errors", registry=registry)
hospital_patient_readmissions_total = Counter("hospital_patient_readmissions_total", "Patient readmissions total", registry=registry)

wards = ["A","B","C","ICU"]

while True:
    for w in wards:
        hospital_beds_available_gauge.labels(ward=w).set(random.randint(0,30))
    hospital_waiting_room_patients_gauge.set(random.randint(0,120))
    hospital_icu_occupancy_percent_gauge.set(random.uniform(40,95))

    hospital_appointments_completed_total.inc(random.randint(0,20))
    if random.random() < 0.01:
        hospital_medication_errors_total.inc()
    hospital_admissions_total.inc(random.randint(0,15))
    hospital_discharges_total.inc(random.randint(0,15))

    hospital_er_wait_time_minutes_histogram.observe(random.uniform(2,180))
    hospital_surgery_duration_minutes_summary.observe(random.uniform(20,480))

    hospital_ventilators_in_use_gauge.set(random.randint(0,60))
    hospital_med_supplies_remaining_gauge.set(random.randint(0,10000))
    hospital_emergency_calls_total.inc(random.randint(0,5))
    hospital_staff_on_duty_gauge.set(random.randint(20,300))
    hospital_isolation_rooms_available_gauge.set(random.randint(0,12))
    hospital_icu_admissions_total.inc(random.randint(0,5))
    hospital_telemetry_errors_total.inc(random.randint(0,3))
    hospital_patient_readmissions_total.inc(random.randint(0,3))

    push_to_gateway(PUSHGATEWAY_URL, job="hospital_job", registry=registry)
    time.sleep(5)
