import duckdb
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
        WHERE procesonombre = $1 
        AND fecha_inicio >= CURRENT_DATE - INTERVAL ($2 || ' DAYS')
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
            conn.execute("INSERT INTO process_records VALUES ($1, $2, $3, $4, $5, $6)", data)
        
        conn.close()
        return len(sample_data)