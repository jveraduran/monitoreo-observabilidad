#!/usr/bin/env python3
"""
Banking metrics simulator - Structured metric names (style B)
Generates 22+ metrics and pushes to Pushgateway job=bank_job
"""
from prometheus_client import CollectorRegistry, Gauge, Counter, Histogram, Summary, push_to_gateway
import random, time

PUSHGATEWAY_URL = "http://localhost:9091"
registry = CollectorRegistry()

# Gauges
bank_atm_cash_available_usd_gauge = Gauge("bank_atm_cash_available_usd_gauge", "Cash available in ATM USD", ["atm_id"], registry=registry)
bank_online_active_users_gauge = Gauge("bank_online_active_users_gauge", "Online banking active users", registry=registry)
bank_system_queue_length_gauge = Gauge("bank_system_queue_length_gauge", "Internal processing queue length", registry=registry)

# Counters
bank_transactions_total_count = Counter("bank_transactions_total_count", "Processed transactions total", ["type"], registry=registry)
bank_card_declines_total = Counter("bank_card_declines_total", "Card declines total", registry=registry)
bank_fraud_attempts_total = Counter("bank_fraud_attempts_total", "Fraud attempts total", registry=registry)
bank_wire_transfers_total = Counter("bank_wire_transfers_total", "Wire transfers total", registry=registry)
bank_login_failures_total = Counter("bank_login_failures_total", "Failed logins total", registry=registry)

# Histograms
bank_transaction_latency_seconds_histogram = Histogram(
    "bank_transaction_latency_seconds_histogram",
    "Transaction latency seconds",
    buckets=[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5],
    registry=registry
)

# Summaries
bank_withdrawal_amount_usd_summary = Summary("bank_withdrawal_amount_usd_summary", "Withdrawal amounts USD summary", registry=registry)
bank_deposit_amount_usd_summary = Summary("bank_deposit_amount_usd_summary", "Deposit amounts USD summary", registry=registry)

# Extra metrics to reach >20
bank_account_openings_total = Counter("bank_account_openings_total", "New accounts opened", registry=registry)
bank_account_closures_total = Counter("bank_account_closures_total", "Accounts closed", registry=registry)
bank_daily_balance_gauge = Gauge("bank_daily_balance_gauge", "Aggregate daily balances USD", registry=registry)
bank_atm_transactions_total = Counter("bank_atm_transactions_total", "ATM transactions total", ["atm_id"], registry=registry)
bank_high_value_alerts_total = Counter("bank_high_value_alerts_total", "High value transaction alerts", registry=registry)
bank_mobile_app_crashes_total = Counter("bank_mobile_app_crashes_total", "Mobile app crashes", registry=registry)
bank_credit_approvals_total = Counter("bank_credit_approvals_total", "Credit approvals", registry=registry)

atm_ids = ["atm-001","atm-002","atm-003"]
tx_types = ["deposit","withdrawal","transfer","payment"]

while True:
    # Gauges
    for atm in atm_ids:
        bank_atm_cash_available_usd_gauge.labels(atm_id=atm).set(random.uniform(2000,50000))
    bank_online_active_users_gauge.set(random.randint(1000,8000))
    bank_system_queue_length_gauge.set(random.randint(0,300))

    # Counters / events
    tx_type = random.choice(tx_types)
    bank_transactions_total_count.labels(type=tx_type).inc(random.randint(0,30))
    if random.random() < 0.03:
        bank_card_declines_total.inc(random.randint(1,5))
    if random.random() < 0.01:
        bank_fraud_attempts_total.inc()
    bank_wire_transfers_total.inc(random.randint(0,5))
    bank_login_failures_total.inc(random.randint(0,20))

    bank_transaction_latency_seconds_histogram.observe(random.expovariate(1/0.08))
    bank_withdrawal_amount_usd_summary.observe(random.choice([random.uniform(20,500), random.uniform(1000,20000)]))
    bank_deposit_amount_usd_summary.observe(random.uniform(10,5000))

    bank_account_openings_total.inc(random.randint(0,3))
    bank_account_closures_total.inc(random.randint(0,2))
    bank_daily_balance_gauge.set(random.uniform(1e6,5e7))
    bank_atm_transactions_total.labels(atm_id=random.choice(atm_ids)).inc(random.randint(0,50))
    if random.random() < 0.005:
        bank_high_value_alerts_total.inc()
    bank_mobile_app_crashes_total.inc(random.randint(0,2))
    bank_credit_approvals_total.inc(random.randint(0,5))

    push_to_gateway(PUSHGATEWAY_URL, job="bank_job", registry=registry)
    time.sleep(5)
