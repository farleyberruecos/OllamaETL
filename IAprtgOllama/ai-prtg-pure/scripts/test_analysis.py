#!/usr/bin/env python3
import sys
import os
import asyncio
sys.path.append('/app')

from core.intelligent_analyzer import IntelligentAnalyzer
from core.data_processor import DataProcessor

async def main():
    print("🧠 Probando análisis 100% puro por IA...")
    
    analyzer = IntelligentAnalyzer(model="llama3.2:1b")  # ✅ CAMBIADO
    processor = DataProcessor()
    
    await analyzer.initialize()
    
    test_processes = ['etl_diario', 'etl_nocturno']
    
    for process in test_processes:
        print(f"\n🔍 Proceso: {process}")
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
        print("\n" + "="*40)
    
    print("\n✅ Prueba completada!")

if __name__ == "__main__":
    asyncio.run(main())