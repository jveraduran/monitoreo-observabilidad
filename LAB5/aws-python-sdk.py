import boto3
import random
import datetime

# --- 1. Define tus credenciales (Generalmente obtenidas de un proveedor de credenciales o ambiente) ---
# NOTA: En un entorno de producción, nunca se deberían codificar
# estas credenciales directamente en el script.
AWS_ACCESS_KEY_ID = 'TU_ACCESS_KEY_AQUI'
AWS_SECRET_ACCESS_KEY = 'TU_SECRET_KEY_AQUI'
AWS_SESSION_TOKEN = 'TU_SESSION_TOKEN_AQUI' # Necesario si usas credenciales temporales (STS/IAM Role)
AWS_REGION = 'us-east-1' # Reemplaza con tu región, e.g., 'eu-central-1'

# Inicializa el cliente de CloudWatch
cloudwatch = boto3.client(
    'cloudwatch',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN
)

# Constantes para las métricas
NAMESPACE = 'AplicacionPython'
INSTANCE_ID_DIMENSION = 'i-0123456789abcdef0' 
CURRENT_TIMESTAMP = datetime.datetime.utcnow()

# --- 2. Generación de las 20 Métricas ---
metric_data_list = []

# --- GRUPO A: Uso de Recursos del Sistema (8 Métricas) ---

# 1. Uso de Disco (Tu métrica original)
metric_data_list.append({
    'MetricName': 'DiskUsedPercent', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': 75.5,
    'Unit': 'Percent'
})
# 2. Inodes Usados
metric_data_list.append({
    'MetricName': 'InodesUsedPercent', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': 45.1,
    'Unit': 'Percent'
})
# 3. Uso de CPU (Usuario)
metric_data_list.append({
    'MetricName': 'CPU_User', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(20, 50),
    'Unit': 'Percent'
})
# 4. Uso de CPU (Sistema)
metric_data_list.append({
    'MetricName': 'CPU_System', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(5, 15),
    'Unit': 'Percent'
})
# 5. Uso de Memoria (Libre)
metric_data_list.append({
    'MetricName': 'Memory_Available', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(1024, 4096),
    'Unit': 'Megabytes'
})
# 6. Uso de Swap
metric_data_list.append({
    'MetricName': 'SwapUsedPercent', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(0, 5),
    'Unit': 'Percent'
})
# 7. Carga del Sistema (1 Minuto)
metric_data_list.append({
    'MetricName': 'Load_Average_1min', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(0.5, 2.0),
    'Unit': 'Count'
})
# 8. Número de Procesos Ejecutándose
metric_data_list.append({
    'MetricName': 'ProcessesRunning', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(100, 250),
    'Unit': 'Count'
})

# --- GRUPO B: Métricas de Red y Tráfico (6 Métricas) ---

# 9. Conexiones TCP Abiertas
metric_data_list.append({
    'MetricName': 'TCPConnectionsEstablished', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(50, 200),
    'Unit': 'Count'
})
# 10. Paquetes de Entrada (Incoming)
metric_data_list.append({
    'MetricName': 'NetworkPacketsIn', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(500, 1500),
    'Unit': 'Count'
})
# 11. Paquetes de Salida (Outgoing)
metric_data_list.append({
    'MetricName': 'NetworkPacketsOut', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(200, 1000),
    'Unit': 'Count'
})
# 12. Errores de Red (Input)
metric_data_list.append({
    'MetricName': 'NetworkErrorsIn', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(0, 5),
    'Unit': 'Count'
})
# 13. Tasa de peticiones HTTP (Global)
metric_data_list.append({
    'MetricName': 'RequestsPerSecond', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(10, 80),
    'Unit': 'Count'
})
# 14. Latencia Promedio de la API (en Segundos)
metric_data_list.append({
    'MetricName': 'APILatency', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(0.05, 0.5),
    'Unit': 'Seconds'
})

# --- GRUPO C: Métricas de Aplicación/Procesamiento (6 Métricas) ---

# 15. Tareas en Cola de Procesamiento
metric_data_list.append({
    'MetricName': 'QueueLength', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(0, 15),
    'Unit': 'Count'
})
# 16. Errores 5xx de la Aplicación
metric_data_list.append({
    'MetricName': 'HTTP5xxCount', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(0, 3),
    'Unit': 'Count'
})
# 17. Tiempo de Procesamiento del Backend (ms)
metric_data_list.append({
    'MetricName': 'BackendProcessingTime', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(100, 800),
    'Unit': 'Milliseconds'
})
# 18. Tasa de Aciertos en Caché
metric_data_list.append({
    'MetricName': 'CacheHitRatio', 
    'Dimensions': [{'Name': 'CacheName', 'Value': 'AppCache'}], # Diferente dimensión
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(85, 99),
    'Unit': 'Percent'
})
# 19. Sesiones de Usuario Activas
metric_data_list.append({
    'MetricName': 'ActiveUserSessions', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.randint(10, 100),
    'Unit': 'Count'
})
# 20. Uso de Hilos/Workers (Pool Size)
metric_data_list.append({
    'MetricName': 'WorkerThreadUsage', 
    'Dimensions': [{'Name': 'InstanceId', 'Value': INSTANCE_ID_DIMENSION}],
    'Timestamp': CURRENT_TIMESTAMP,
    'Value': random.uniform(50, 95),
    'Unit': 'Percent'
})

# --- 3. Llamada Final a la API de CloudWatch ---
print(f"Enviando {len(metric_data_list)} métricas a CloudWatch...")

response = cloudwatch.put_metric_data(
    Namespace=NAMESPACE,
    MetricData=metric_data_list
)

print("Métricas enviadas con éxito:", response)