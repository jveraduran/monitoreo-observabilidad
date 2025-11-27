// Importa las clases y funciones necesarias del SDK de AWS
import { CloudWatchClient, PutMetricDataCommand } from "@aws-sdk/client-cloudwatch";

// --- 1. CONFIGURACIÓN DE CREDENCIALES Y REGIÓN ---
// NOTA: Para producción, se recomienda usar roles de IAM o variables de entorno
// La función 'process.env' lee las variables de entorno de tu terminal
const AWS_REGION = process.env.AWS_REGION || "us-east-1"; 
const AWS_ACCESS_KEY_ID = "TU_ACCESS_KEY_AQUI"; // Reemplaza
const AWS_SECRET_ACCESS_KEY = "TU_SECRET_KEY_AQUI"; // Reemplaza
const AWS_SESSION_TOKEN = "TU_SESSION_TOKEN_AQUI"; // Reemplaza (si usas STS/credenciales temporales)

// Inicializa el cliente de CloudWatch
const client = new CloudWatchClient({
    region: AWS_REGION,
    credentials: {
        accessKeyId: AWS_ACCESS_KEY_ID,
        secretAccessKey: AWS_SECRET_ACCESS_KEY,
        sessionToken: AWS_SESSION_TOKEN,
    }
});

// Constantes para las métricas
const NAMESPACE = 'AplicacionNodejs';
const INSTANCE_ID_DIMENSION = 'i-0123456789abcdef0';
const CURRENT_TIMESTAMP = new Date();

// Función de utilidad para generar un valor aleatorio flotante
function getRandomFloat(min, max) {
    return (Math.random() * (max - min) + min).toFixed(2);
}

// --- 2. GENERACIÓN DE LAS 20 MÉTRICAS ---
const metricDataList = [
    // --- GRUPO A: Uso de Recursos (8 Métricas) ---
    {
        MetricName: 'DiskUsedPercent', Value: getRandomFloat(60, 80), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'InodesUsedPercent', Value: getRandomFloat(40, 50), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'CPU_User', Value: getRandomFloat(20, 50), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'CPU_System', Value: getRandomFloat(5, 15), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'Memory_Available', Value: Math.floor(getRandomFloat(1024, 4096)), Unit: 'Megabytes',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'SwapUsedPercent', Value: getRandomFloat(0, 5), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'Load_Average_1min', Value: getRandomFloat(0.5, 2.0), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'ProcessesRunning', Value: Math.floor(getRandomFloat(100, 250)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },

    // --- GRUPO B: Métricas de Red y Tráfico (6 Métricas) ---
    {
        MetricName: 'TCPConnectionsEstablished', Value: Math.floor(getRandomFloat(50, 200)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'NetworkPacketsIn', Value: Math.floor(getRandomFloat(500, 1500)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'NetworkPacketsOut', Value: Math.floor(getRandomFloat(200, 1000)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'NetworkErrorsIn', Value: Math.floor(getRandomFloat(0, 5)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'RequestsPerSecond', Value: Math.floor(getRandomFloat(10, 80)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'APILatency', Value: getRandomFloat(0.05, 0.5), Unit: 'Seconds',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },

    // --- GRUPO C: Métricas de Aplicación/Procesamiento (6 Métricas) ---
    {
        MetricName: 'QueueLength', Value: Math.floor(getRandomFloat(0, 15)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'HTTP5xxCount', Value: Math.floor(getRandomFloat(0, 3)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'BackendProcessingTime', Value: Math.floor(getRandomFloat(100, 800)), Unit: 'Milliseconds',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'CacheHitRatio', Value: getRandomFloat(85, 99), Unit: 'Percent',
        Dimensions: [{ Name: 'CacheName', Value: 'AppCache' }] // Dimensión diferente
    },
    {
        MetricName: 'ActiveUserSessions', Value: Math.floor(getRandomFloat(10, 100)), Unit: 'Count',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
    {
        MetricName: 'WorkerThreadUsage', Value: getRandomFloat(50, 95), Unit: 'Percent',
        Dimensions: [{ Name: 'InstanceId', Value: INSTANCE_ID_DIMENSION }]
    },
];

// Asignar el timestamp a todas las métricas
const MetricDataWithTimestamp = metricDataList.map(metric => ({
    ...metric,
    Timestamp: CURRENT_TIMESTAMP
}));

// --- 3. FUNCIÓN PARA ENVIAR LA DATA ---

const sendMetrics = async () => {
    console.log(`Intentando enviar ${MetricDataWithTimestamp.length} métricas al namespace ${NAMESPACE}...`);
    
    const command = new PutMetricDataCommand({
        Namespace: NAMESPACE,
        MetricData: MetricDataWithTimestamp,
    });

    try {
        const response = await client.send(command);
        console.log("Métricas enviadas con éxito:", response);
        // La respuesta exitosa generalmente solo contiene ResponseMetadata (HTTP 200)
    } catch (error) {
        console.error("Error al enviar métricas a CloudWatch:", error);
    }
};

sendMetrics();