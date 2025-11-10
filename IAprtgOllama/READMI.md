# AI-PRTG Pure Intelligence - Documentación Completa

## Tabla de Contenidos
- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Módulos del Sistema](#-módulos-del-sistema)
- [Guía de Implementación](#-guía-de-implementación)
- [Uso de la API](#-uso-de-la-api)
- [Configuración Avanzada](#-configuración-avanzada)
- [Solución de Problemas](#-solución-de-problemas)
- [Escalabilidad y Producción](#-escalabilidad-y-producción)
- [Casos de Uso](#-casos-de-uso)
- [Mantenimiento](#-mantenimiento)

## Descripción del Proyecto

**AI-PRTG Pure Intelligence** es un sistema de análisis inteligente que utiliza IA 100% pura (Ollama) para analizar datos de procesos ETL. A diferencia de sistemas tradicionales, **NO usa algoritmos predefinidos** - todo el análisis lo realiza la IA basándose únicamente en los datos crudos.

**Características principales:**
- Análisis 100% por IA sin reglas predefinidas
- Soporte para múltiples modelos de Ollama
- API RESTful completa
- Base de datos embebida DuckDB
- Contenerización completa con Docker
- Datos de ejemplo realistas

## Arquitectura del Sistema

``` 
ai-prtg-pure/
├──  docker-compose.yml # Orquestación de contenedores
├──  api/
│ ├── app.py # API principal FastAPI
│ ├── requirements.txt # Dependencias Python
│ └── Dockerfile # Contenedor de la API
├──  core/
│ ├── intelligent_analyzer.py # Motor de IA pura
│ └── data_processor.py # Gestor de datos
├── data/
│ └── processing.db # Base de datos DuckDB
└──  scripts/
├── init_db.py # Inicializador de BD
└── test_analysis.py # Pruebas del sistema
```


## 🔧 Módulos del Sistema

### 1. Orchestration Layer (`docker-compose.yml`)

**Propósito**: Gestiona los contenedores Docker del sistema

**Servicios:**
- **`ollama`**: Contenedor de IA (Ollama)
  - Puerto: `11434`
  - Memoria: 8GB
  - Volumen persistente para modelos
  
- **`api`**: Contenedor de la API FastAPI
  - Puerto: `8000`
  - Depende de Ollama
  - Monta volúmenes para datos y código

### 2. API Layer (`api/`)

**Propósito**: Exponer endpoints REST para análisis inteligente

**Archivos principales:**
- **`app.py`**: API FastAPI con endpoints
- **`requirements.txt`**: Dependencias Python
- **`Dockerfile`**: Contenedor de la aplicación

**Endpoints disponibles:**
- `POST /analyze` - Análisis completo por IA
- `POST /detect-anomalies` - Detección de anomalías
- `POST /predict` - Predicción de tendencias
- `GET /health` - Estado del sistema

### 3. Core Intelligence Layer (`core/`)

#### `intelligent_analyzer.py` - Motor de IA Pura

**Características:**
- Conexión asíncrona con Ollama
- Análisis 100% basado en IA sin reglas predefinidas
- Soporte para múltiples modelos de Ollama
- Manejo de timeouts y errores

**Métodos principales:**
- `analyze_process_intelligently()` - Análisis general
- `detect_anomalies_intelligently()` - Detección de anomalías
- `predict_trend_intelligently()` - Predicción de tendencias

#### `data_processor.py` - Gestor de Datos

**Características:**
- Conexión con DuckDB (base de datos embebida)
- Generación de datos de ejemplo realistas
- Consultas optimizadas para análisis temporal

### 4. Data Layer (`data/`)

**Estructura de datos:**
```sql
process_records:
- id_key (VARCHAR) - Identificador único
- fecha_inicio (TIMESTAMP) - Inicio de ejecución
- fecha_fin (TIMESTAMP) - Fin de ejecución
- tiempo_duracion (DOUBLE) - Duración en minutos
- registros_procesados (INTEGER) - Volumen procesado
- procesonombre (VARCHAR) - Nombre del proceso

## AI-PRTG - Comandos Principales

##  Comandos Esenciales para Ejecutar el Proyecto

### Inicialización y Construcción
| Comando | Descripción | Ejemplo de Uso |
|---------|-------------|----------------|
| `docker-compose build --no-cache` | Reconstruir imágenes desde cero | Cuando hay cambios en dependencias |
| `docker-compose up -d` | Iniciar todos los servicios en segundo plano | Al empezar a trabajar |
| `docker-compose down` | Detener y eliminar todos los servicios | Al terminar de trabajar |

### Gestión de Datos
| Comando | Descripción | Ejemplo de Uso |
|---------|-------------|----------------|
| `docker-compose exec api python scripts/init_db.py` | Crear base de datos con datos de ejemplo | Primera vez o para resetear datos |
| `docker-compose exec api python scripts/test_analysis.py` | Ejecutar prueba completa del sistema | Verificar que todo funciona |

### Operación y Monitoreo
| Comando | Descripción | Ejemplo de Uso |
|---------|-------------|----------------|
| `docker-compose ps` | Ver estado de los contenedores | Verificar que todo esté corriendo |
| `docker-compose logs -f api` | Ver logs en tiempo real de la API | Cuando hay errores o para debug |
| `docker-compose restart api` | Reiniciar solo el servicio de API | Después de cambios en el código |

### Uso de la API
| Comando | Descripción | Ejemplo de Uso |
|---------|-------------|----------------|
| `curl http://localhost:8000/health` | Verificar estado del sistema | Confirmar que la API responde |
| `curl -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d '{"process_name": "etl_diario", "lookback_days": 7}'` | Analizar un proceso específico | Obtener análisis de IA |

##  Comandos de Mantenimiento
| Comando | Descripción | Cuándo Usarlo |
|---------|-------------|---------------|
| `docker-compose restart` | Reiniciar todos los servicios | Después de cambios de configuración |
| `docker-compose logs --tail=50` | Ver últimas 50 líneas de logs | Para debugging rápido |
| `docker-compose exec api bash` | Acceder a terminal del contenedor API | Para troubleshooting avanzado |

##  Flujo de Trabajo Típico

```bash
# 1. Construir/Reconstruir el proyecto
docker-compose build --no-cache

# 2. Iniciar servicios
docker-compose up -d

# 3. Inicializar datos
docker-compose exec api python scripts/init_db.py

# 4. Ejecutar pruebas
docker-compose exec api python scripts/test_analysis.py

# 5. Usar la API
curl -X POST "http://localhost:8000/analyze" -H "Content-Type: application/json" -d '{"process_name": "etl_diario", "lookback_days": 7}'