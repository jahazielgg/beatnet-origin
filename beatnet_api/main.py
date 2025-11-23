"""
BeatNet System - Main Application
FastAPI + Algoritmos de Grafos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path

from api.routes import router

# Crear directorios necesarios
Path("data").mkdir(exist_ok=True)
Path("outputs").mkdir(exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="BeatNet API",
    description="""
    Sistema de recomendación de música usando algoritmos de grafos.
    
    **Algoritmos implementados:**
    - **Similitud**: Fuerza Bruta O(n²), Optimizaciones
    - **Ordenamiento**: MergeSort, QuickSort, QuickSelect
    - **Búsqueda en Grafos**: BFS, DFS, Dijkstra
    - **Recomendaciones**: Backtracking para playlists óptimas
    - **Visualización**: Graphviz para representación gráfica
    
    **Pasos para usar:**
    1. POST /load - Cargar datos y construir grafo
    2. GET /songs - Ver canciones disponibles
    3. GET /recommendations/{song_id} - Obtener recomendaciones
    4. POST /playlist/optimal - Generar playlist óptima
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(router, prefix="/api/v1", tags=["BeatNet Endpoints"])

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Endpoint de health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "BeatNet API is running"}

# Ejecutar aplicación
if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║               BeatNet System              ║
    ║                                            ║
    ║  Algoritmos implementados:                 ║
    ║  ✓ Fuerza Bruta O(n²)                     ║
    ║  ✓ Backtracking para playlists            ║
    ║  ✓ BFS, DFS, Dijkstra                     ║
    ║  ✓ MergeSort, QuickSort, QuickSelect      ║
    ║  ✓ Visualización con Graphviz             ║
    ║                                            ║
    ║  Documentación: http://localhost:8000/docs ║
    ╚════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )