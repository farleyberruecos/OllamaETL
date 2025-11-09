import asyncio
import aiohttp
import pandas as pd
import json
from typing import Dict, Any

class IntelligentAnalyzer:
    def __init__(self, model: str = "llama3.2:1b"):
        """
        Inicializar el analizador inteligente
        
        Args:
            model: Modelo de Ollama a utilizar
                  Ejemplos: "llama3.2:1b", "llama3.2:1b", "mistral", "llama2"
        """
        self.ollama_url = "http://ollama:11434"
        self.model = model  # ⭐ MODELO CONFIGURABLE AQUÍ ⭐
        self.initialized = False
    
    async def initialize(self):
        """Inicializar conexión con Ollama"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags") as response:
                    if response.status == 200:
                        self.initialized = True
                        print(f"🧠 Ollama inicializado - Modelo: {self.model}")
                        print("✅ Sistema inteligente listo")
                    else:
                        print("⚠️  Ollama no disponible")
        except Exception as e:
            print(f"❌ Error conectando con Ollama: {e}")
    
    async def analyze_process_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Análisis Solo datos crudos + IA
        """
        try:
            # Solo pasar los datos crudos en formato simple
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Analiza los siguientes datos de ejecuciones de los '{process_name}'  que es un proceso de carga incremental ETL:

            {raw_data}

            Responde brevemente: Con respecto a la ultima ejecucion(útima fecha), ¿Qué patrones identificas aplicando analitica en los datos(estadistica y probabilidades?
            el resultado debe ser un json estructurado.
            """
            
            print(f"🔍 Enviando análisis para {process_name}...")
            analysis = await self._query_ollama_pure(prompt)
            return {"raw_analysis": analysis}
            
        except Exception as e:
            return {"error": f"Análisis falló: {str(e)}"}
    
    async def detect_anomalies_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Detección 
        """
        try:
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Revisa estos datos de '{process_name}':

            {raw_data}

            Señala solo 1-2 patrones inusuales si estos existen de forma  brevemente y estructurada 
            con respuesto a la ultima ejecucion identificada en los datos, entregar la respuesta estructurada en un json:
            """
            
            print(f"🔍 Detectando anomalías para {process_name}...")
            anomalies = await self._query_ollama_pure(prompt)
            return {"anomaly_detection": anomalies}
            
        except Exception as e:
            return {"error": f"Detección falló: {str(e)}"}
    
    async def predict_trend_intelligently(self, data: pd.DataFrame, process_name: str) -> Dict[str, Any]:
        """
        Predicción 
        """
        try:
            raw_data = self._get_raw_data_only(data, process_name)
            
            prompt = f"""
            Basándote en estos datos de '{process_name}' con respecto a la última ejecución:

            {raw_data}

            Predicción breve para el futuro como seria su comportamiento aplicar series de tiempo entregar de forma estructurada en un json:
            """
            
            print(f"🔍 Prediciendo tendencias para {process_name}...")
            prediction = await self._query_ollama_pure(prompt)
            return {"trend_prediction": prediction}
            
        except Exception as e:
            return {"error": f"Predicción falló: {str(e)}"}
    
    def _get_raw_data_only(self, data: pd.DataFrame, process_name: str) -> str:
        """Solo devolver los datos crudos sin procesar"""
        if data.empty:
            return "No hay datos"
        
        # Limitar a 10 registros máximo para evitar prompts muy largos
        data_limited = data.head(10000)
        
        # Simplemente mostrar los datos tal cual
        raw_text = f"Proceso: {process_name}\n"
        raw_text += f"Total de registros: {len(data_limited)}\n\n"
        
        # Mostrar datos con limite
        for i, row in data_limited.iterrows():
            raw_text += f"Ejecución {i+1}:\n"
            raw_text += f"  Inicio: {row['fecha_inicio']}\n"
            raw_text += f"  Duración: {row['tiempo_duracion']} min\n"
            raw_text += f"  Registros: {row['registros_procesados']:,}\n"
            raw_text += f"  Hora: {pd.to_datetime(row['fecha_inicio']).hour}:00\n"
            raw_text += "\n"
        
        return raw_text
    
    async def _query_ollama_pure(self, prompt: str, model: str = None) -> str:
        """
        Consulta  Ollama 
        
        Args:
            prompt: Texto para enviar al modelo
            model: Modelo específico (opcional, usa self.model por defecto)
        """
        # Usar el modelo de la instancia si no se especifica uno
        if model is None:
            model = self.model
            
        try:
            print(f"🤖 Consultando modelo: {model}")
            print(f"📝 Longitud prompt: {len(prompt)} caracteres")
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as session:  # 300 segundos
                async with session.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,  # Reducida para más consistencia
                            "top_p": 0.8,        # Reducida
                            "top_k": 20,         # Reducida
                            "num_predict": 200   # Limitar respuesta
                        }
                    }
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get('response', 'Sin respuesta del modelo')
                        print(f"✅ Respuesta recibida: {len(response_text)} caracteres")
                        return response_text
                    else:
                        error_text = await response.text()
                        print(f"❌ Error HTTP: {response.status} - {error_text}")
                        return f"Error Ollama ({response.status}): {error_text}"
                        
        except asyncio.TimeoutError:
            print(f"⏰ Timeout después de 300 segundos con modelo: {model}")
            return f"Timeout: El modelo {model} no respondió en 300 segundos"
        except Exception as e:
            print(f"💥 Error de conexión: {e}")
            return f"Error de conexión con {model}: {str(e)}"
    
    async def health_check(self) -> bool:
        """Verificar estado del servicio"""
        return self.initialized
    
    def get_model_info(self) -> str:
        """Obtener información del modelo configurado"""
        return f"Modelo configurado: {self.model}"