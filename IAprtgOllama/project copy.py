import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PureAIPRTGGenerator:
    def __init__(self, project_name="ai-prtg-pure"):
        self.project_name = project_name
        self.base_dir = project_name
        
    def create_complete_structure(self):
        """Crea la estructura completa del proyecto"""
        try:
            # Crear directorios principales
            directories = [
                self.base_dir,
                f"{self.base_dir}/api",
                f"{self.base_dir}/core", 
                f"{self.base_dir}/data",
                f"{self.base_dir}/scripts"
            ]
            
            for directory in directories:
                os.makedirs(directory, exist_ok=True)
                logger.info(f"📁 Directorio creado: {directory}")
            
            # Crear todos los archivos
            self._create_docker_compose()
            self._create_api_files()
            self._create_core_files()
            self._create_script_files()
            
            logger.info(f"✅ Proyecto {self.project_name} creado exitosamente!")
            self._print_instructions()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creando estructura: {e}")
            return False

    def _print_instructions(self):
        """Imprime instrucciones de uso"""
        print("\n" + "="*60)
        print("🚀 AI-PRTG PURO - ESTRUCTURA CREADA")
        print("="*60)
        print("\n📁 Estructura creada:")
        print(f"{self.project_name}/")
        print("├── 🐳 docker-compose.yml")
        print("├── 🚀 api/")
        print("│   ├── app.py")
        print("│   ├── requirements.txt")
        print("│   └── Dockerfile")
        print("├── 🧠 core/")
        print("│   ├── intelligent_analyzer.py")
        print("│   └── data_processor.py")
        print("├── 📊 data/")
        print("└── 📜 scripts/")
        print("    ├── init_db.py")
        print("    └── test_analysis.py")
        
        print("\n🚀 COMANDOS PARA EJECUTAR:")
        print(f"1. cd {self.project_name}")
        print("2. docker-compose up -d")
        print("3. docker exec ai-prtg-api python scripts/init_db.py")
        print("4. docker exec ai-prtg-api python scripts/test_analysis.py")
        
        print("\n🌐 URLs:")
        print("• API: http://localhost:8000")
        print("• Ollama: http://localhost:11434")
        print("="*60)

    def _create_docker_compose(self):
        """Crea docker-compose.yml"""
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
          memory: 8G
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
      - ./core:/app/core
      - ./data:/app/data
      - ./scripts:/app/scripts
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    networks:
      - ai-prtg-network

volumes:
  ollama_data:

networks:
  ai-prtg-network:
    driver: bridge
"""
        with open(f"{self.base_dir}/docker-compose.yml", "w") as f:
            f.write(content)
        logger.info("📄 docker-compose.yml creado")

    def _create_api_files(self):
        """Crea archivos de la API"""
        
        # requirements.txt
        requirements = """fastapi==0.104.1
uvicorn==0.24.0
duckdb==0.9.2
pandas==2.1.3
aiohttp==3.9.1
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
        
        # app.py
        app_content = '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import duckdb
import pandas as pd
from datetime import datetime
import asyncio

from core.intelligent_analyzer import IntelligentAnalyzer
from core.data_processor import DataProcessor

app = FastAPI(title="AI-PRTG Pure Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = IntelligentAnalyzer()
data_processor = DataProcessor()

class AnalysisRequest(BaseModel):
    process_name: str
    lookback_days: int = 7

@app.on_event("startup")
async def startup_event():
    await analyzer.initialize()

@app.get("/")
async def root():
    return {"message": "AI-PRTG - Análisis 100% por IA", "version": "1.0"}

@app.post("/analyze")
async def analyze_process(request: AnalysisRequest):
    """Análisis puro por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, f"No hay datos para: {request.process_name}")
        
        analysis = await analyzer.analyze_process_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "timestamp": datetime.now().isoformat(),
            "data_points": len(data),
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.post("/detect-anomalies")
async def detect_anomalies(request: AnalysisRequest):
    """Detección pura por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, "No hay datos")
        
        anomalies = await analyzer.detect_anomalies_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "anomalies": anomalies
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.post("/predict")
async def predict_trend(request: AnalysisRequest):
    """Predicción pura por IA"""
    try:
        data = data_processor.get_detailed_data(request.process_name, request.lookback_days)
        
        if data.empty:
            raise HTTPException(404, "No hay datos")
        
        prediction = await analyzer.predict_trend_intelligently(data, request.process_name)
        
        return {
            "process": request.process_name,
            "prediction": prediction
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")

@app.get("/health")
async def health_check():
    try:
        conn = duckdb.connect('./data/processing.db')
        db_ok = conn.execute("SELECT 1").fetchone() is not None
        conn.close()
        
        ollama_ok = await analyzer.health_check()
        
        return {
            "status": "healthy" if all([db_ok, ollama_ok]) else "degraded",
            "database": "online" if db_ok else "offline",
            "ollama": "online" if ollama_ok else "offline"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        with open(f"{self.base_dir}/api/app.py", "w") as f:
            f.write(app_content)
        
        logger.info("📄 Archivos de API creados")

    def _create_core_files(self):
        """Crea los archivos core"""
        
        # intelligent_analyzer.py
        intelligent_analyzer = '''import asyncio
import aiohttp
import pandas as pd
import json
from typing import Dict, Any

class IntelligentAnalyzer:
    def __init__(self):
        self.ollama_url = "http://ollama:11434"
        self.initialized = False
    
    async def initialize(self):
        """Inicializar conexión con Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags") as response:
                    if response.status == 200:
                        self.initialized = True
                        print("🧠 Ollama inicializado - Sistema inteligente listo")
                    else:
                        print("⚠️  Ollama no disponible")
        except Exception as e:
            print(f"❌ Error conectando con Ollama: {e}")
    
    async def analyze_process_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Análisis 100% puro - Solo datos crudos + IA
        """
        try:
            # Solo pasar los datos crudos en formato simple
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Aquí tienes datos crudos de un proceso ETL llamado '{process_name}'.
            
            DATOS CRUDOS:
            {raw_data}

            Por favor analiza estos datos con tu inteligencia natural.
            Observa lo que veas interesante, inusual o importante.
            No hay reglas, no hay guías, solo datos y tu análisis.
            """
            
            analysis = await self._query_ollama_pure(prompt)
            return {"raw_analysis": analysis}
            
        except Exception as e:
            return {"error": f"Análisis falló: {str(e)}"}
    
    async def detect_anomalies_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Detección 100% pura - Solo datos crudos + IA
        """
        try:
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Aquí tienes datos crudos del proceso '{process_name}'.
            
            DATOS:
            {raw_data}

            Mira estos datos y dime qué te parece inusual o anómalo.
            Usa solo tu criterio e intuición.
            """
            
            anomalies = await self._query_ollama_pure(prompt)
            return {"anomaly_detection": anomalies}
            
        except Exception as e:
            return {"error": f"Detección falló: {str(e)}"}
    
    async def predict_trend_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Predicción 100% pura - Solo datos crudos + IA
        """
        try:
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Aquí tienes datos históricos del proceso '{process_name}'.
            
            DATOS:
            {raw_data}

            Basándote solo en estos datos, ¿qué crees que pasará en el futuro?
            Da tu opinión intuitiva.
            """
            
            prediction = await self._query_ollama_pure(prompt)
            return {"trend_prediction": prediction}
            
        except Exception as e:
            return {"error": f"Predicción falló: {str(e)}"}
    
    def _get_raw_data_only(self, data: pd.DataFrame, process_name: str) -> str:
        """Solo devolver los datos crudos sin procesar"""
        if data.empty:
            return "No hay datos"
        
        # Simplemente mostrar los datos tal cual
        raw_text = f"Proceso: {process_name}\\n"
        raw_text += f"Total de registros: {len(data)}\\n\\n"
        
        # Mostrar todos los datos crudos
        for i, row in data.iterrows():
            raw_text += f"Ejecución {i+1}:\\n"
            raw_text += f"  Inicio: {row['fecha_inicio']}\\n"
            raw_text += f"  Fin: {row['fecha_fin']}\\n"
            raw_text += f"  Duración: {row['tiempo_duracion']} minutos\\n"
            raw_text += f"  Registros: {row['registros_procesados']:,}\\n"
            raw_text += f"  Hora: {pd.to_datetime(row['fecha_inicio']).hour}:00\\n"
            raw_text += f"  Día semana: {pd.to_datetime(row['fecha_inicio']).day_name()}\\n"
            raw_text += "\\n"
        
        return raw_text
    
    async def _query_ollama_pure(self, prompt: str, model: str = "llama3.2:1b") -> str:
        """Consulta pura a Ollama - solo texto libre"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.9,  # Máxima creatividad
                            "top_p": 0.95,
                            "top_k": 60
                        }
                    }
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        return result['response']
                    else:
                        return "Ollama no respondió"
                        
        except Exception as e:
            return f"Error de conexión: {str(e)}"
    
    async def health_check(self) -> bool:
        return self.initialized
'''
        with open(f"{self.base_dir}/core/intelligent_analyzer.py", "w") as f:
            f.write(intelligent_analyzer)

        # data_processor.py
        data_processor = '''import duckdb
import pandas as pd
from datetime import datetime, timedelta
import random

class DataProcessor:
    def __init__(self, db_path: str = "./data/processing.db"):
        self.db_path = db_path
    
    def get_detailed_data(self, process_name: str, days: int = 7) -> pd.DataFrame:
        """Obtener datos crudos"""
        conn = duckdb.connect(self.db_path)
        
        query = """
        SELECT 
            id_key,
            fecha_inicio,
            fecha_fin,
            tiempo_duracion,
            registros_procesados,
            procesonombre
        FROM process_records 
        WHERE procesonombre = ? 
        AND fecha_inicio >= CURRENT_DATE - INTERVAL ? DAY
        ORDER BY fecha_inicio
        """
        
        df = conn.execute(query, [process_name, days]).df()
        conn.close()
        
        return df
    
    def insert_sample_data(self):
        """Insertar datos de ejemplo variados"""
        conn = duckdb.connect(self.db_path)
        
        conn.execute("""
        CREATE TABLE IF NOT EXISTS process_records (
            id_key VARCHAR PRIMARY KEY,
            fecha_inicio TIMESTAMP,
            fecha_fin TIMESTAMP,
            tiempo_duracion DOUBLE,
            registros_procesados INTEGER,
            procesonombre VARCHAR
        )
        """)
        
        conn.execute("DELETE FROM process_records")
        
        sample_data = []
        base_date = datetime.now() - timedelta(days=60)
        
        # Procesos con comportamientos diferentes
        processes = [
            {'name': 'etl_diario', 'duration_range': (20, 40), 'volume_range': (100000, 200000)},
            {'name': 'etl_nocturno', 'duration_range': (35, 55), 'volume_range': (250000, 350000)},
            {'name': 'etl_fin_semana', 'duration_range': (45, 75), 'volume_range': (300000, 450000)},
        ]
        
        record_id = 0
        
        for process in processes:
            for day_offset in range(60):
                current_date = base_date + timedelta(days=day_offset)
                
                # Comportamientos naturales
                if process['name'] == 'etl_diario':
                    hour = random.randint(8, 11)
                    executions = 1
                elif process['name'] == 'etl_nocturno':
                    hour = random.randint(20, 23)
                    executions = 1
                elif process['name'] == 'etl_fin_semana':
                    hour = random.randint(10, 18)
                    executions = 1 if current_date.weekday() >= 5 else 0
                else:
                    executions = 0
                
                for execution in range(executions):
                    record_id += 1
                    
                    duration = random.uniform(process['duration_range'][0], process['duration_range'][1])
                    volume = random.randint(process['volume_range'][0], process['volume_range'][1])
                    
                    # Algunas variaciones interesantes
                    if record_id % 25 == 0:
                        duration *= 2  # Más largo
                    if record_id % 30 == 0:
                        volume = int(volume * 0.3)  # Más bajo
                    
                    fecha_inicio = current_date.replace(hour=hour, minute=random.randint(0, 59))
                    fecha_fin = fecha_inicio + timedelta(minutes=duration)
                    
                    sample_data.append((
                        f"proc_{record_id:06d}",
                        fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                        fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
                        duration,
                        volume,
                        process['name']
                    ))
        
        # Insertar datos
        print(f"📊 Insertando {len(sample_data)} registros...")
        
        for data in sample_data:
            conn.execute("INSERT INTO process_records VALUES (?, ?, ?, ?, ?, ?)", data)
        
        conn.close()
        return len(sample_data)
'''
        with open(f"{self.base_dir}/core/data_processor.py", "w") as f:
            f.write(data_processor)
        
        logger.info("📄 Archivos core creados")

    def _create_script_files(self):
        """Crea los scripts"""
        
        # init_db.py
        init_db = '''#!/usr/bin/env python3
import sys
import os
sys.path.append('/app')

from core.data_processor import DataProcessor

def main():
    print("🗃️  Inicializando base de datos...")
    
    processor = DataProcessor()
    records_inserted = processor.insert_sample_data()
    
    print(f"✅ Base de datos inicializada con {records_inserted} registros")
    print("📊 Procesos disponibles: etl_diario, etl_nocturno, etl_fin_semana")

if __name__ == "__main__":
    main()
'''
        with open(f"{self.base_dir}/scripts/init_db.py", "w") as f:
            f.write(init_db)

        # test_analysis.py
        test_analysis = '''#!/usr/bin/env python3
import sys
import os
import asyncio
sys.path.append('/app')

from core.intelligent_analyzer import IntelligentAnalyzer
from core.data_processor import DataProcessor

async def main():
    print("🧠 Probando análisis 100% puro por IA...")
    
    analyzer = IntelligentAnalyzer()
    processor = DataProcessor()
    
    await analyzer.initialize()
    
    test_processes = ['etl_diario', 'etl_nocturno']
    
    for process in test_processes:
        print(f"\\n🔍 Proceso: {process}")
        print("="*40)
        
        data = processor.get_detailed_data(process, 30)
        
        if data.empty:
            print(f"❌ Sin datos")
            continue
        
        print(f"📊 {len(data)} ejecuciones")
        print("🤖 IA analizando...")
        
        analysis = await analyzer.analyze_process_intelligently(data, process)
        
        print("💡 ANÁLISIS DE LA IA:")
        print(analysis.get('raw_analysis', 'No analysis'))
        print("\\n" + "="*40)
    
    print("\\n✅ Prueba completada!")

if __name__ == "__main__":
    asyncio.run(main())
'''
        with open(f"{self.base_dir}/scripts/test_analysis.py", "w") as f:
            f.write(test_analysis)
        
        logger.info("📄 Scripts creados")

# Ejecutar el generador
if __name__ == "__main__":
    generator = PureAIPRTGGenerator("ai-prtg-pure")
    success = generator.create_complete_structure()
    
    if success:
        print(f"\\n🎉 ¡Proyecto creado exitosamente en la carpeta 'ai-prtg-pure'!")
        print("🚀 Ahora puedes ejecutar los comandos mostrados arriba.")
    else:
        print("❌ Error creando el proyecto")