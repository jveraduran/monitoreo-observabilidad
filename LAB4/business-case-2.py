#!/usr/bin/env python3
"""
banking_push.py

Simulador de métricas bancarias que hace PUSH a Pushgateway.
Genera métricas (counters, gauges, histograms) y las envía usando
pushadd_to_gateway para no sobrescribir series previas, permitiendo la
recolección constante por Prometheus.

Requisitos:
    pip install prometheus_client

Uso:
    python3 banking_push.py --instance <instance-name> --pushgateway http://localhost:9091 --interval 5
"""

import time
import random
import argparse
from prometheus_client import CollectorRegistry, Counter, Gauge, Histogram, pushadd_to_gateway

def build_registry(registry):
    # 1. Transacciones y Negocio Central
    registry.bank_transaction_total = Counter(
        "bank_transaction_total", "Total de transacciones procesadas", ["type", "status", "channel"], registry=registry
    )
    registry.bank_transaction_value_total = Counter(
        "bank_transaction_value_total", "Valor monetario total procesado (en centavos)", ["type"], registry=registry
    )
    registry.bank_new_accounts_total = Counter(
        "bank_new_accounts_total", "Total de nuevas cuentas abiertas", ["product"], registry=registry
    )
    registry.bank_payments_processing_time_seconds = Histogram(
        "bank_payments_processing_time_seconds", "Latencia de procesamiento de pagos interbancarios", 
        buckets=[0.1, 1, 5, 10, 60], registry=registry
    )

    # 2. Originación de Crédito y Riesgo
    registry.credit_application_total = Counter(
        "credit_application_total", "Total de solicitudes de crédito recibidas", ["product_type"], registry=registry
    )
    registry.credit_application_approved_total = Counter(
        "credit_application_approved_total", "Solicitudes aprobadas", ["product_type"], registry=registry
    )
    registry.credit_application_latency_seconds = Histogram(
        "credit_application_latency_seconds", "Latencia desde la aplicación hasta la decisión final", 
        buckets=[5, 30, 120, 300, 1800], registry=registry
    )
    registry.bank_npl_ratio = Gauge(
        "bank_npl_ratio", "Ratio de Préstamos No Productivos (NPL)", registry=registry
    )

    # 3. Cajeros Automáticos (ATM)
    registry.atm_transaction_total = Counter(
        "atm_transaction_total", "Transacciones totales en ATMs", ["operation"], registry=registry
    )
    registry.atm_out_of_service_total = Counter(
        "atm_out_of_service_total", "Eventos de cajeros fuera de servicio", ["reason"], registry=registry
    )
    registry.atm_device_status = Gauge(
        "atm_device_status", "Estado binario del dispositivo (1=activo, 0=inactivo)", ["device_id"], registry=registry
    )
    registry.atm_cash_level_percent = Gauge(
        "atm_cash_level_percent", "Nivel de efectivo restante en el cajero (0-100)", ["device_id"], registry=registry
    )

    # 4. Seguridad y Fraude
    registry.security_login_success_total = Counter(
        "security_login_success_total", "Inicios de sesión exitosos", ["channel"], registry=registry
    )
    registry.security_login_failed_total = Counter(
        "security_login_failed_total", "Intentos de login fallidos", ["reason"], registry=registry
    )
    registry.security_fraud_alerts_total = Counter(
        "security_fraud_alerts_total", "Alertas generadas por sistema de fraude", ["severity"], registry=registry
    )

    # 5. Backend / APIs
    registry.api_requests_total = Counter(
        "api_requests_total", "Total de requests a APIs del core bancario", ["service","code"], registry=registry
    )
    registry.api_latency_seconds = Histogram(
        "api_latency_seconds", "Latencia de endpoints", buckets=[0.005, 0.05, 0.1, 0.5, 1], registry=registry
    )
    registry.db_query_time_seconds = Histogram(
        "db_query_time_seconds", "Latencia de consultas DB", buckets=[0.001, 0.005, 0.01, 0.05], registry=registry
    )

    return registry

def simulate_and_push(args):
    registry = CollectorRegistry()
    registry = build_registry(registry)

    channels = ["web", "mobile", "api"]
    atm_devices = [f"ATM-{i:03d}" for i in range(1, 4)]
    credit_types = ["personal", "hipotecario", "auto"]
    api_services = ["accounts", "payments", "auth"]

    # Estado persistente para Gauges que no son de infra (ej. NPL)
    npl_value = 0.025 # Inicializamos NPL

    while True:
        # --- 1. Transacciones y Negocio Central ---
        for ch in channels:
            attempts = random.randint(100, 500)
            successes = int(attempts * random.uniform(0.95, 0.995))
            failures = attempts - successes
            
            # Transferencias
            registry.bank_transaction_total.labels(type="transfer", status="success", channel=ch).inc(successes)
            registry.bank_transaction_total.labels(type="transfer", status="failed", channel=ch).inc(failures)
            registry.bank_transaction_value_total.labels(type="transfer").inc(successes * random.randint(1000, 50000))

            # Apertura de cuentas (Simulado como un evento batch o menos frecuente)
            if random.random() < 0.1:
                registry.bank_new_accounts_total.labels(product="checking").inc(1)
            
            # Latencia de pagos interbancarios (simulando un worker)
            for _ in range(random.randint(0, 5)):
                registry.bank_payments_processing_time_seconds.observe(random.uniform(0.1, 5.0))

        # --- 2. Originación de Crédito y Riesgo ---
        for ctype in credit_types:
            applications = random.randint(1, 10)
            approved = int(applications * random.uniform(0.5, 0.8))
            registry.credit_application_total.labels(product_type=ctype).inc(applications)
            registry.credit_application_approved_total.labels(product_type=ctype).inc(approved)
            
            for _ in range(applications):
                registry.credit_application_latency_seconds.observe(random.uniform(10, 600))

        # NPL (se simula un pequeño cambio que se "push" de un proceso diario)
        npl_value += random.uniform(-0.0005, 0.0005)
        registry.bank_npl_ratio.set(round(npl_value, 4))
        
        # --- 3. Cajeros Automáticos (ATM) ---
        for device in atm_devices:
            # Estado y Cash Level (Gauges)
            status = 1 if random.random() > 0.1 else 0 # 10% de probabilidad de fallo
            registry.atm_device_status.labels(device_id=device).set(status)
            registry.atm_cash_level_percent.labels(device_id=device).set(random.uniform(10, 95))

            # Transacciones y fallos (Counters)
            if status == 1:
                registry.atm_transaction_total.labels(operation="withdrawal").inc(random.randint(5, 20))
            else:
                registry.atm_out_of_service_total.labels(reason="hardware_fail").inc(1)

        # --- 4. Seguridad y Fraude ---
        for ch in channels:
            registry.security_login_success_total.labels(channel=ch).inc(random.randint(10, 100))
        registry.security_login_failed_total.labels(reason="credentials_fail").inc(random.randint(1, 5))
        if random.random() < 0.05:
            registry.security_fraud_alerts_total.labels(severity="critical").inc(1)

        # --- 5. Backend / APIs ---
        for svc in api_services:
            reqs = random.randint(50, 500)
            errors = int(reqs * random.uniform(0.00, 0.01))
            registry.api_requests_total.labels(service=svc, code="200").inc(reqs - errors)
            if errors > 0:
                registry.api_requests_total.labels(service=svc, code="500").inc(errors) # 5xx es un request total que falla
            # Latency samples
            for _ in range(min(reqs // 50, 10)):
                registry.api_latency_seconds.observe(random.uniform(0.01, 0.5))
        
        # DB Latency (general pool)
        for _ in range(random.randint(5, 20)):
            registry.db_query_time_seconds.observe(random.uniform(0.0005, 0.05))

        # --- Push al Pushgateway ---
        instance = args.instance or "bank-sim-core-1"
        try:
            pushadd_to_gateway(
                args.pushgateway,
                job=args.job,
                registry=registry,
                grouping_key={"instance": instance}
            )
            print(f"Pushed metrics to {args.pushgateway} (job={args.job}, instance={instance}) at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error pushing to Pushgateway: {e}")

        time.sleep(args.interval)

def main():
    parser = argparse.ArgumentParser(description="Banking metrics simulator (push to Pushgateway)")
    parser.add_argument("--pushgateway", default="http://localhost:9091", help="Pushgateway URL")
    parser.add_argument("--job", default="banking_core_job", help="Pushgateway job name")
    parser.add_argument("--instance", default="bank-sim-core-1", help="Instance label to push (grouping_key)")
    parser.add_argument("--interval", type=int, default=5, help="Seconds between pushes")
    args = parser.parse_args()

    # Inicializa el estado para que los contadores no se resetee con cada llamada a build_registry
    simulate_and_push(args)

if __name__ == "__main__":
    main()