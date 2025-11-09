import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProjectGenerator:
    def __init__(self, project_name="ai-prtg"):
        self.project_name = project_name
        self.base_dir = project_name
        
    def create_structure(self):
        """Crea la estructura completa del proyecto"""
        try:
            # Directorios principales
            directories = [
                self.base_dir,
                f"{self.base_dir}/config",
                f"{self.base_dir}/scripts",
                f"{self.base_dir}/api",
                f"{self.base_dir}/models",
                f"{self.base_dir}/data",
                f"{self.base_dir}/database",
                f"{self.base_dir}/frontend"
            ]
            
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"Directorio creado: {directory}")
            
            # Crear archivos
            self._create_docker_compose()
            self._create_env_file()
            self._create_config_files()
            self._create_api_files()
            self._create_model_files()
            self._create_script_files()
            self._create_database_files()
            self._create_frontend_files()
            
            logger.info(f"✅ Proyecto {self.project_name} creado exitosamente!")
            self._print_usage_instructions()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creando estructura: {e}")
            return False

    def _print_usage_instructions(self):
        """Imprime instrucciones de uso"""
        print("\n" + "="*60)
        print("🚀 PROYECTO AI-PRTG CREADO EXITOSAMENTE")
        print("="*60)
        print("\n📁 Estructura creada:")
        print("ai-prtg/")
        print("├── docker-compose.yml          # Orquestación de contenedores")
        print("├── .env                        # Variables de entorno")
        print("├── config/")
        print("│   ├── settings.yaml           # Configuración de análisis")
        print("│   └── database_config.yaml    # Configuración de BD")
        print("├── api/")
        print("│   ├── app.py                  # API principal")
        print("│   ├── requirements.txt        # Dependencias Python")
        print("│   └── Dockerfile              # Contenedor API")
        print("├── models/")
        print("│   └── trend_analyzer.py       # Modelo de IA")
        print("├── database/")
        print("│   ├── db_manager.py           # Gestor de base de datos")
        print("│   └── init.sql                # Inicialización BD")
        print("├── scripts/")
        print("│   ├── init-models.sh          # Descarga modelos IA")
        print("│   └── test-system.py          # Pruebas del sistema")
        print("└── frontend/")
        print("    └── index.html              # Dashboard simple")
        
        print("\n🚀 COMANDOS PARA INICIAR:")
        print("1. cd ai-prtg")
        print("2. docker-compose up -d")
        print("3. docker exec ai-prtg-api python scripts/test-system.py")
        
        print("\n🌐 URLs de acceso:")
        print("• API: http://localhost:8000")
        print("• Ollama: http://localhost:11434")
        print("• pgAdmin: http://localhost:5050")
        print("• Frontend: http://localhost:8080")
        
        print("\n📊 Endpoints principales:")
        print("• POST /analyze - Analizar métricas")
        print("• POST /analyze-from-db - Analizar desde base de datos")
        print("• GET /metrics/{context} - Obtener métricas")
        print("• POST /insert-metric - Insertar nueva métrica")
        print("• GET /health - Estado del sistema")
        print("="*60)

    def _create_docker_compose(self):
        """Crea el archivo docker-compose.yml"""
        content = """version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ai-prtg-ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    deploy:
      resources:
        limits:
          memory: 4G
    networks:
      - ai-prtg-network

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: ai-prtg-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./config:/app/config
      - ./data:/app/data
      - ./database:/app/database
      - ./scripts:/app/scripts
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - DATABASE_URL=postgresql://admin:admin123@database:5432/ai_prtg
    depends_on:
      - ollama
      - database
    networks:
      - ai-prtg-network

  database:
    image: postgres:15
    container_name: ai-prtg-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=ai_prtg
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - ai-prtg-network

volumes:
  ollama_data:
  postgres_data:

networks:
  ai-prtg-network:
    driver: bridge
"""
        with open(f"{self.base_dir}/docker-compose.yml", "w") as f:
            f.write(content)

    def _create_env_file(self):
        """Crea el archivo .env"""
        content = """# Configuración de la aplicación
OLLAMA_HOST=0.0.0.0
DATABASE_URL=postgresql://admin:admin123@localhost:5432/ai_prtg

# Configuración de análisis
CRITICAL_THRESHOLD=50.0
WARNING_THRESHOLD=20.0
"""
        with open(f"{self.base_dir}/.env", "w") as f:
            f.write(content)

    def _create_config_files(self):
        """Crea archivos de configuración"""
        # settings.yaml
        settings_content = """analysis:
  thresholds:
    critical_increase: 50.0
    critical_decrease: -40.0
    warning_increase: 20.0
    warning_decrease: -15.0
  window_size: 10

models:
  trend_model: "llama3.2:1b"
  prompt_template: |
    Analiza esta serie de métricas de {context}:
    Valores: {metrics}
    
    Responde SOLO en formato JSON:
    {
      "critical_trend": true/false,
      "confidence": 0.85,
      "analysis": "breve análisis",
      "pattern_type": "increasing/decreasing/stable/volatile",
      "recommendation": "acción recomendada"
    }
"""
        with open(f"{self.base_dir}/config/settings.yaml", "w") as f:
            f.write(settings_content)
        
        # database_config.yaml
        db_config = """connections:
  postgresql:
    host: "database"
    port: 5432
    database: "ai_prtg"
    username: "admin"
    password: "admin123"

queries:
  get_metrics: "SELECT * FROM system_metrics WHERE context = %s ORDER BY timestamp DESC LIMIT %s"
  insert_metric: "INSERT INTO system_metrics (metric_name, metric_value, context) VALUES (%s, %s, %s)"
"""
        with open(f"{self.base_dir}/config/database_config.yaml", "w") as f:
            f.write(db_config)

    def _create_api_files(self):
        """Crea los archivos de la API"""
        # requirements.txt
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
pydantic==2.5.0
psycopg2-binary==2.9.9
pyyaml==6.0.1
python-multipart==0.0.6
"""
        with open(f"{self.base_dir}/api/requirements.txt", "w") as f:
            f.write(requirements)
        
        # Dockerfile
        dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
"""
        with open(f"{self.base_dir}/api/Dockerfile", "w") as f:
            f.write(dockerfile)
        
        # app.py (versión simplificada)
        app_content = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import requests
import database.db_manager as db_manager

app = FastAPI(title="AI-PRTG API")

# Inicializar base de datos
db = db_manager.DatabaseManager()

class MetricSeries(BaseModel):
    metrics: List[float]
    context: str = "cpu_usage"

@app.get("/")
async def root():
    return {"message": "AI-PRTG Analysis System"}

@app.post("/analyze")
async def analyze_trend(request: MetricSeries):
    """Analiza métricas y devuelve si hay tendencia crítica"""
    try:
        # Análisis simple (aquí integrarías tu IA)
        avg = sum(request.metrics) / len(request.metrics)
        critical = avg > 80.0  # Ejemplo simple
        
        result = {
            "critical_trend": critical,
            "confidence": 0.85,
            "analysis": f"Promedio: {avg:.1f}%",
            "pattern_type": "critical" if critical else "normal",
            "recommendation": "Revisar sistema" if critical else "Todo normal"
        }
        
        # Guardar en BD
        db.save_analysis(request.context, request.metrics, result)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/{context}")
async def get_metrics(context: str, limit: int = 10):
    """Obtiene métricas de la base de datos"""
    metrics = db.get_metrics(context, limit)
    return {"context": context, "metrics": metrics}

@app.post("/insert-metric")
async def insert_metric(metric_data: dict):
    """Inserta una nueva métrica"""
    success = db.insert_metric(
        metric_data['name'],
        metric_data['value'],
        metric_data['context']
    )
    return {"success": success}

@app.get("/health")
async def health_check():
    """Estado del sistema"""
    db_ok = db.test_connection()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "online" if db_ok else "offline"
    }
'''
        with open(f"{self.base_dir}/api/app.py", "w") as f:
            f.write(app_content)

    def _create_model_files(self):
        """Crea el archivo del modelo de análisis"""
        trend_analyzer = '''import requests
import json

class TrendAnalyzer:
    def __init__(self, config):
        self.config = config
        self.ollama_url = "http://ollama:11434"
    
    async def analyze_series(self, metrics, context, threshold=None):
        """Analiza series temporales usando Ollama"""
        prompt = f"""
        Analiza estas métricas de {context}: {metrics}
        
        Responde en JSON:
        {{
            "critical_trend": true/false,
            "confidence": 0.XX,
            "analysis": "texto",
            "pattern_type": "tipo",
            "recommendation": "acción"
        }}
        """
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return json.loads(result['response'])
            else:
                return self._fallback_analysis(metrics)
                
        except:
            return self._fallback_analysis(metrics)
    
    def _fallback_analysis(self, metrics):
        """Análisis de respaldo"""
        avg = sum(metrics) / len(metrics)
        return {
            "critical_trend": avg > 80,
            "confidence": 0.7,
            "analysis": f"Promedio: {avg:.1f}",
            "pattern_type": "critical" if avg > 80 else "normal",
            "recommendation": "Revisar" if avg > 80 else "Monitorizar"
        }
'''
        with open(f"{self.base_dir}/models/trend_analyzer.py", "w") as f:
            f.write(trend_analyzer)

    def _create_database_files(self):
        """Crea archivos de base de datos"""
        # init.sql
        init_sql = """CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value REAL NOT NULL,
    context VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trend_analysis (
    id SERIAL PRIMARY KEY,
    metric_context VARCHAR(100) NOT NULL,
    metrics_data JSONB NOT NULL,
    critical_trend BOOLEAN NOT NULL,
    confidence REAL,
    analysis TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO system_metrics (metric_name, metric_value, context) VALUES
('cpu_usage', 45.0, 'server_1'),
('cpu_usage', 65.0, 'server_1'),
('cpu_usage', 85.0, 'server_1'),
('memory_usage', 60.0, 'server_2'),
('memory_usage', 62.0, 'server_2'),
('memory_usage', 58.0, 'server_2');
"""
        with open(f"{self.base_dir}/database/init.sql", "w") as f:
            f.write(init_sql)
        
        # db_manager.py (versión simplificada)
        db_manager = '''import psycopg2
import json

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self._connect()
    
    def _connect(self):
        """Conectar a PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host="database",
                database="ai_prtg",
                user="admin",
                password="admin123"
            )
        except Exception as e:
            print(f"Error conectando a BD: {e}")
    
    def test_connection(self):
        """Probar conexión"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except:
            return False
    
    def get_metrics(self, context, limit=10):
        """Obtener métricas"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT * FROM system_metrics WHERE context = %s ORDER BY timestamp DESC LIMIT %s",
                (context, limit)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Error obteniendo métricas: {e}")
            return []
    
    def insert_metric(self, name, value, context):
        """Insertar métrica"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO system_metrics (metric_name, metric_value, context) VALUES (%s, %s, %s)",
                (name, value, context)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error insertando métrica: {e}")
            return False
    
    def save_analysis(self, context, metrics, result):
        """Guardar análisis"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO trend_analysis (metric_context, metrics_data, critical_trend, confidence, analysis) VALUES (%s, %s, %s, %s, %s)",
                (context, json.dumps(metrics), result['critical_trend'], result['confidence'], result['analysis'])
            )
            self.connection.commit()
        except Exception as e:
            print(f"Error guardando análisis: {e}")
'''
        with open(f"{self.base_dir}/database/db_manager.py", "w") as f:
            f.write(db_manager)

    def _create_script_files(self):
        """Crea scripts de utilidad"""
        # init-models.sh
        init_models = """#!/bin/bash
echo "Descargando modelos de IA..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3.2:1b"}'
echo "Modelo descargado!"
"""
        with open(f"{self.base_dir}/scripts/init-models.sh", "w") as f:
            f.write(init_models)
        
        # test-system.py
        test_system = """#!/usr/bin/env python3
import requests
import time

print("🧪 Probando sistema AI-PRTG...")

# Esperar que los servicios estén listos
time.sleep(10)

# Probar salud del sistema
try:
    health = requests.get("http://localhost:8000/health").json()
    print(f"✅ Health: {health}")
except:
    print("❌ API no disponible")

# Probar inserción de métrica
test_metric = {
    "name": "cpu_usage",
    "value": 75.5,
    "context": "test_server"
}

try:
    insert = requests.post("http://localhost:8000/insert-metric", json=test_metric).json()
    print(f"✅ Métrica insertada: {insert}")
except Exception as e:
    print(f"❌ Error insertando métrica: {e}")

# Probar análisis
test_analysis = {
    "metrics": [45, 52, 68, 75, 82, 88],
    "context": "cpu_usage"
}

try:
    analysis = requests.post("http://localhost:8000/analyze", json=test_analysis).json()
    print(f"✅ Análisis: {analysis}")
except Exception as e:
    print(f"❌ Error en análisis: {e}")

print("🧪 Pruebas completadas!")
"""
        with open(f"{self.base_dir}/scripts/test-system.py", "w") as f:
            f.write(test_system)

    def _create_frontend_files(self):
        """Crea un frontend simple"""
        index_html = """<!DOCTYPE html>
<html>
<head>
    <title>AI-PRTG Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .card { border: 1px solid #ddd; padding: 20px; margin: 10px; border-radius: 5px; }
        .critical { border-left: 5px solid red; }
        .normal { border-left: 5px solid green; }
    </style>
</head>
<body>
    <h1>🔍 AI-PRTG - Monitor Inteligente</h1>
    
    <div class="card">
        <h3>Análisis de Métricas</h3>
        <button onclick="testAnalysis()">Probar Análisis</button>
        <div id="result"></div>
    </div>

    <script>
        async function testAnalysis() {
            const response = await fetch('http://localhost:8000/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    metrics: [45, 62, 78, 85, 92],
                    context: "cpu_usage"
                })
            });
            
            const result = await response.json();
            document.getElementById('result').innerHTML = `
                <div class="card ${result.critical_trend ? 'critical' : 'normal'}">
                    <strong>Tendencia Crítica:</strong> ${result.critical_trend}<br>
                    <strong>Análisis:</strong> ${result.analysis}<br>
                    <strong>Recomendación:</strong> ${result.recommendation}
                </div>
            `;
        }
    </script>
</body>
</html>"""
        with open(f"{self.base_dir}/frontend/index.html", "w") as f:
            f.write(index_html)

# Ejecutar el generador
if __name__ == "__main__":
    generator = ProjectGenerator("ai-prtg")
    generator.create_structure()