# 1. Levantar servicios (si no están corriendo)
docker-compose up -d

# 2. Verificar que el modelo está disponible (OPCIONAL - ya lo vimos que sí)
curl http://localhost:11434/api/tags

# 3. Inicializar base de datos
docker exec ai-prtg-api python scripts/init_db.py

# 4. Ejecutar prueba
docker exec ai-prtg-api python scripts/test_analysis.py