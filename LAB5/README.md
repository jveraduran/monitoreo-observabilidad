# 📈 Clase IX: Métricas Personalizadas y Automatización en CloudWatch

Este repositorio contiene la guía práctica y los scripts necesarios para la **Clase IX: Métricas Personalizadas y Automatización en CloudWatch**. Aprenderás a publicar métricas desde aplicaciones de usuario (Python y Node.js) y a configurar la infraestructura de monitoreo básica.

---

## 🧭 Tabla de Contenidos

1.  [Conceptos Clave](#1-conceptos-clave)
2.  [Prerrequisitos](#2-prerrequisitos)
3.  [Configuración del Entorno](#3-configuración-del-entorno)
    * [3.1. AWS CLI y Credenciales](#31-aws-cli-y-credenciales)
    * [3.2. Instalación de Python](#32-instalación-de-python)
    * [3.3. Instalación de Node.js (Debian)](#33-instalación-de-nodejs-debian)
4.  [Ejecución de Scripts de Envío de Métricas](#4-ejecución-de-scripts-de-envío-de-métricas)
    * [4.1. Python (Boto3)](#41-python-boto3)
    * [4.2. Node.js (AWS SDK)](#42-nodejs-aws-sdk)

---

## 1. Conceptos Clave

* **Métrica Personalizada:** Cualquier punto de datos que una aplicación o sistema envía a CloudWatch que no es recopilado automáticamente por AWS (ej. uso de disco, transacciones por segundo de una API).
* **Namespace:** Un contenedor lógico para las métricas personalizadas. Es el nivel más alto de organización (ej. `MiAplicacion/Observabilidad`).
* **`put_metric_data`:** Es el comando (API) utilizado por los SDKs de AWS para enviar uno o más puntos de datos de métricas a CloudWatch.
* **Boto3:** El SDK oficial de AWS para el lenguaje **Python**.
* **AWS SDK for JavaScript:** El SDK utilizado en entornos **Node.js** para interactuar con los servicios de AWS.

---

## 2. Prerrequisitos

Para completar esta guía, necesitarás lo siguiente:

* **Una cuenta de AWS activa.**
* **Permisos de IAM:** Un usuario o rol con permisos para ejecutar la acción `cloudwatch:PutMetricData`.
* **Sistema Operativo:** Una máquina local o una instancia EC2 con **Debian/Ubuntu** instalada para los comandos de Node.js.
* **Archivos de Script:** Debes tener los siguientes archivos listos en tu directorio de trabajo:
    * `aws-python-sdk.py` (Script de envío de métricas en Python)
    * `aws-nodejs.js` (Script de envío de métricas en Node.js)
    * `package.json` (Archivo de configuración de dependencias de Node.js)

---

## 3. Configuración del Entorno

### 3.1. AWS CLI y Credenciales

Antes de ejecutar cualquier script, debes configurar tus credenciales de AWS. Se recomienda el uso de **credenciales temporales** o **Roles de IAM**, pero si ejecutas localmente, puedes usar la CLI:

1.  **Instala la AWS CLI** (si aún no lo has hecho).
2.  **Configura un perfil** con tu Access Key y Secret Key. La región debe coincidir con la configurada en los scripts.
    ```bash
    aws configure
    # Ingresa: AWS Access Key ID, AWS Secret Access Key, Default region name
    ```
    > **Nota:** Si usas `aws configure`, no necesitas codificar las credenciales en los scripts Python/Node.js.

### 3.2. Instalación de Python

Estos comandos instalarán la última versión de Python, `pip` y el soporte para entornos virtuales.


1. Actualizar el índice de paquetes e instalar dependencias
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

2. Verificar la instalación
```bash
python3 --version
pip3 --version
```

Preparación del Entorno Virtual y Boto3:

Utilizaremos un entorno virtual para aislar las dependencias del proyecto.

1. Crear el entorno virtual (llamado 'venv')
```bash
python3 -m venv venv
```

2. Activar el entorno virtual
```bash
source venv/bin/activate
```
3. Instalar la librería Boto3 (AWS SDK para Python)
```bash
pip install boto3
```

#### 3.3. Instalación de Node.js (Debian)

Instalaremos Node.js (versión 20.x LTS) y npm utilizando el repositorio oficial de NodeSource.

1. Actualizar el sistema e instalar dependencias clave
```bash
sudo apt update
sudo apt upgrade
sudo apt install curl gnupg2 -y
```

2. Agregar el repositorio de Node.js 20.x LTS
```bash
curl -fsSL [https://deb.nodesource.com/setup_20.x](https://deb.nodesource.com/setup_20.x) | sudo -E bash -
```
3. Instalar Node.js y npm
```bash
sudo apt install nodejs -y
```

4. Verificar la instalación
```bash
node -v
npm -v
```

5. Inicializar el proyecto y dependencias de Node.js
```bash
npm init -y # Crea el package.json (Solo en caso de no existir un package.json)
npm install @aws-sdk/client-cloudwatch # Solo en caso de no existir un package-lock.json
```

---
## 4. Ejecución de Scripts de Envío de Métricas

### 4.1. Python (Boto3)

Script: aws-python-sdk.py (Envía 20 métricas al namespace MiAplicacion/UsoDisco o similar).

1. Asegúrate de que tu entorno virtual esté activo ((venv) debe aparecer en tu prompt).

2. Ejecuta el script:
```bash
python3 aws-python-sdk.py
```

### 4.2. Node.js (AWS SDK)

Script: aws-nodejs.js (Envía 20 métricas al namespace AplicacionNodejs).

1. Asegúrate de que tus credenciales de AWS estén configuradas (ya sea vía aws configure o variables de entorno).

2. Ejecuta el script:
```bash
node aws-nodejs.js
```
---

## 🚀 Siguientes Pasos
Una vez ejecutados los scripts, verifica las métricas en la consola de AWS:

1. Navega a la consola de Amazon CloudWatch.
2. Ve a Métricas $\rightarrow$ Todas las métricas.
3. Busca los namespaces:
    - MiAplicacion/UsoDisco (Métricas de Python)
    - AplicacionNodejs (Métricas de Node.js)

4. Crea un Dashboard que muestre la correlación entre el DiskUsedPercent y el HTTP5xxCount para mejorar la observabilidad.