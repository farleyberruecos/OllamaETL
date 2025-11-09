#!/usr/bin/env python3
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
