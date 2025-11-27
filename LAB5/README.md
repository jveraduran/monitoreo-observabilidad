# Métricas Personalizadas y Automatización en CloudWatch


## Enviar métricas Python:

Instalar python:

``` bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
``` 

Crear entorno virtual:
``` bash
python3 -m venv venv
source venv/bin/activate
``` 

Instalar librería boto3:
``` bash
pip install boto3
```

``` bash
python3 aws-python-sdk.py
``` 

## Enviar Metricas Node

```bash
sudo apt update
sudo apt upgrade
``` 

```
sudo apt install curl gnupg2 -y
```

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y
```

```bash
node -v
npm -v
```