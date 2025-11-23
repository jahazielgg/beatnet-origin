"""
FastAPI Routes - Endpoints de la API
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
from pydantic import BaseModel

from services.data_service import DataService
from services.visualization_service import VisualizationService
from core.similarity import find_most_similar
from core.search import bfs_search, dfs_search, dijkstra_shortest_path, find_connected_components
from core.sorting import merge_sort, quick_sort, get_top_k_songs
from core.recommendations import find_optimal_playlist, generate_diverse_playlist, greedy_playlist

# Instancia global del servicio de datos
data_service = DataService()

# Router de FastAPI
router = APIRouter()

# ============ MODELOS PYDANTIC ============

class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genres: List[str]
    duration: int
    year: Optional[int]
    popularity: int
    preview_url: str
    cover_url: str

class SimilarityResponse(BaseModel):
    song: SongResponse
    similarity: float

class PlaylistResponse(BaseModel):
    songs: List[SongResponse]
    total_similarity: float
    algorithm_used: str

class GraphStatsResponse(BaseModel):
    total_songs: int
    total_connections: int
    average_degree: float
    density: float

class PathResponse(BaseModel):
    path: List[SongResponse]
    total_similarity: float

# ============ ENDPOINTS ============

@router.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "BeatNet API",
        "version": "1.0",
        "endpoints": {
            "songs": "/songs",
            "recommendations": "/recommendations/{song_id}",
            "playlist": "/playlist/optimal",
            "search": "/search/bfs",
            "stats": "/stats"
        }
    }

@router.post("/load")
async def load_data(min_similarity: float = 0.3, max_songs: Optional[int] = None):
    """Carga datos y construye el grafo"""
    try:
        data_service.load_songs()
        data_service.build_graph(min_similarity, max_songs)
        
        stats = data_service.graph.get_statistics()
        
        return {
            "status": "success",
            "message": "Datos cargados y grafo construido",
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/songs", response_model=List[SongResponse])
async def get_all_songs(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("popularity", regex="^(popularity|title|year)$")
):
    """Obtiene lista de canciones con paginación"""
    if not data_service.songs:
        raise HTTPException(status_code=400, detail="No hay datos cargados. Usa POST /load primero")
    
    # Ordenar según criterio
    if sort_by == "popularity":
        sorted_songs = quick_sort(data_service.songs, key=lambda s: s.popularity, reverse=True)
    elif sort_by == "year":
        sorted_songs = quick_sort(data_service.songs, key=lambda s: s.year or 0, reverse=True)
    else:  # title
        sorted_songs = merge_sort(data_service.songs, key=lambda s: s.title.lower())
    
    # Paginación
    paginated = sorted_songs[offset:offset + limit]
    
    return [SongResponse(**song.to_dict()) for song in paginated]

@router.get("/songs/{song_id}", response_model=SongResponse)
async def get_song(song_id: str):
    """Obtiene una canción por ID"""
    song = data_service.get_song_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    
    return SongResponse(**song.to_dict())

@router.get("/songs/search/title")
async def search_by_title(q: str, fuzzy: bool = True):
    """Busca canciones por título"""
    song = data_service.get_song_by_title(q, fuzzy)
    if not song:
        raise HTTPException(status_code=404, detail="No se encontró ninguna canción")
    
    return SongResponse(**song.to_dict())

@router.get("/songs/genre/{genre}", response_model=List[SongResponse])
async def get_songs_by_genre(genre: str, limit: int = Query(50, ge=1, le=200)):
    """Obtiene canciones de un género específico"""
    songs = data_service.get_songs_by_genre(genre)
    if not songs:
        raise HTTPException(status_code=404, detail=f"No se encontraron canciones del género '{genre}'")
    
    return [SongResponse(**s.to_dict()) for s in songs[:limit]]

@router.get("/recommendations/{song_id}", response_model=List[SimilarityResponse])
async def get_recommendations(
    song_id: str,
    top_k: int = Query(10, ge=1, le=50),
    method: str = Query("graph", regex="^(graph|brute_force)$")
):
    """
    Obtiene recomendaciones para una canción
    - method='graph': Usa vecinos del grafo (rápido)
    - method='brute_force': Calcula similitud con todas las canciones
    """
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido. Usa POST /load")
    
    song = data_service.get_song_by_id(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    
    if method == "graph":
        # Usar vecinos del grafo
        neighbors = data_service.graph.get_neighbors(song_id, min_similarity=0.0)
        neighbors = neighbors[:top_k]
        
        return [
            SimilarityResponse(
                song=SongResponse(**neighbor_song.to_dict()),
                similarity=round(sim, 3)
            )
            for neighbor_song, sim in neighbors
        ]
    else:
        # Fuerza bruta
        all_songs = data_service.graph.get_all_songs()
        similar = find_most_similar(song, all_songs, top_k)
        
        return [
            SimilarityResponse(
                song=SongResponse(**similar_song.to_dict()),
                similarity=round(sim, 3)
            )
            for similar_song, sim in similar
        ]

@router.post("/playlist/optimal", response_model=PlaylistResponse)
async def create_optimal_playlist(
    song_id: str,
    length: int = Query(8, ge=2, le=15),  # ← REDUCIDO de 30 a 15
    min_similarity: float = Query(0.35, ge=0.2, le=1.0)  # ← Aumentado mínimo
):
    """
    Crea playlist óptima usando BACKTRACKING
    Encuentra la secuencia con mayor similitud acumulada
    NOTA: Usar length <= 10 para mejor rendimiento
    """
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    if song_id not in data_service.graph.nodes:
        raise HTTPException(status_code=404, detail="Canción no encontrada en el grafo")
    
    # Validación adicional para evitar timeouts
    if length > 12:
        raise HTTPException(
            status_code=400, 
            detail="Para length > 12, el algoritmo puede tardar demasiado. Usa length <= 12"
        )
    
    playlist, total_sim = find_optimal_playlist(
        data_service.graph,
        song_id,
        length,
        min_similarity
    )
    
    if not playlist:
        raise HTTPException(status_code=404, detail="No se pudo generar playlist con los parámetros dados")
    
    return PlaylistResponse(
        songs=[SongResponse(**s.to_dict()) for s in playlist],
        total_similarity=round(total_sim, 3),
        algorithm_used="backtracking"
    )

@router.post("/playlist/diverse", response_model=PlaylistResponse)
async def create_diverse_playlist(
    song_id: str,
    length: int = Query(10, ge=2, le=30),
    diversity_weight: float = Query(0.3, ge=0.0, le=1.0)
):
    """
    Crea playlist balanceando similitud y diversidad
    diversity_weight: 0 = solo similitud, 1 = solo diversidad
    """
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    playlist = generate_diverse_playlist(
        data_service.graph,
        song_id,
        length,
        diversity_weight
    )
    
    if not playlist:
        raise HTTPException(status_code=404, detail="No se pudo generar playlist")
    
    # Calcular similitud total
    total_sim = 0.0
    for i in range(len(playlist) - 1):
        total_sim += playlist[i].similarity_score(playlist[i + 1])
    
    return PlaylistResponse(
        songs=[SongResponse(**s.to_dict()) for s in playlist],
        total_similarity=round(total_sim, 3),
        algorithm_used="diverse_backtracking"
    )

@router.post("/playlist/greedy", response_model=PlaylistResponse)
async def create_greedy_playlist(
    song_id: str,
    length: int = Query(10, ge=2, le=30)
):
    """
    Crea playlist usando algoritmo GREEDY (más rápido, no óptimo)
    Siempre elige el vecino más similar
    """
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    playlist = greedy_playlist(data_service.graph, song_id, length)
    
    if not playlist:
        raise HTTPException(status_code=404, detail="No se pudo generar playlist")
    
    # Calcular similitud total
    total_sim = 0.0
    for i in range(len(playlist) - 1):
        total_sim += playlist[i].similarity_score(playlist[i + 1])
    
    return PlaylistResponse(
        songs=[SongResponse(**s.to_dict()) for s in playlist],
        total_similarity=round(total_sim, 3),
        algorithm_used="greedy"
    )

@router.get("/search/bfs/{song_id}", response_model=List[SongResponse])
async def search_bfs(
    song_id: str,
    max_depth: int = Query(3, ge=1, le=5)
):
    """Búsqueda BFS (Breadth-First Search) desde una canción"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    results = bfs_search(data_service.graph, song_id, max_depth)
    
    return [SongResponse(**s.to_dict()) for s in results]

@router.get("/search/dfs/{song_id}", response_model=List[SongResponse])
async def search_dfs(
    song_id: str,
    max_depth: int = Query(3, ge=1, le=5)
):
    """Búsqueda DFS (Depth-First Search) desde una canción"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    results = dfs_search(data_service.graph, song_id, max_depth)
    
    return [SongResponse(**s.to_dict()) for s in results]

@router.get("/path/{start_id}/{end_id}", response_model=PathResponse)
async def find_path(start_id: str, end_id: str):
    """
    Encuentra el camino más corto entre dos canciones usando Dijkstra
    Maximiza la similitud acumulada
    """
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    result = dijkstra_shortest_path(data_service.graph, start_id, end_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="No existe camino entre las canciones")
    
    path, total_sim = result
    
    return PathResponse(
        path=[SongResponse(**s.to_dict()) for s in path],
        total_similarity=round(total_sim, 3)
    )

@router.get("/stats", response_model=GraphStatsResponse)
async def get_statistics():
    """Obtiene estadísticas del grafo"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    stats = data_service.graph.get_statistics()
    return GraphStatsResponse(**stats)

@router.get("/stats/genres")
async def get_genre_stats():
    """Obtiene estadísticas de géneros"""
    if not data_service.songs:
        raise HTTPException(status_code=400, detail="No hay datos cargados")
    
    return data_service.get_genre_statistics()

@router.get("/stats/artists")
async def get_artist_stats():
    """Obtiene estadísticas de artistas"""
    if not data_service.songs:
        raise HTTPException(status_code=400, detail="No hay datos cargados")
    
    return data_service.get_artist_statistics()

@router.get("/stats/components")
async def get_components():
    """Encuentra componentes conexas del grafo"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    components = find_connected_components(data_service.graph)
    
    return {
        "total_components": len(components),
        "largest_component_size": len(components[0]) if components else 0,
        "component_sizes": [len(comp) for comp in components[:10]]
    }

@router.get("/top/{criteria}")
async def get_top_songs(
    criteria: str = Path(..., regex="^(popularity|duration)$"),
    k: int = Query(10, ge=1, le=100)
):
    """
    Obtiene top K canciones usando QuickSelect (O(n) promedio)
    criteria: 'popularity' o 'duration'
    """
    if not data_service.songs:
        raise HTTPException(status_code=400, detail="No hay datos cargados")
    
    if criteria == "popularity":
        key_func = lambda s: s.popularity
    else:
        key_func = lambda s: s.duration
    
    top_songs = get_top_k_songs(data_service.songs, k, key_func)
    
    return [SongResponse(**s.to_dict()) for s in top_songs]

@router.post("/visualize/full")
async def visualize_full_graph(
    max_nodes: int = Query(50, ge=10, le=200),
    min_similarity: float = Query(0.4, ge=0.0, le=1.0)
):
    """Genera visualización del grafo completo"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    try:
        VisualizationService.generate_full_graph(
            data_service.graph,
            "outputs/full_graph",
            max_nodes,
            min_similarity
        )
        return {"status": "success", "file": "outputs/full_graph.png"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/visualize/subgraph/{song_id}")
async def visualize_subgraph(
    song_id: str,
    depth: int = Query(2, ge=1, le=3),
    max_nodes: int = Query(25, ge=10, le=50)  # ← AGREGADO
):
    """Genera visualización de subgrafo centrado en una canción"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    try:
        VisualizationService.generate_subgraph(
            data_service.graph,
            song_id,
            depth,
            output_path=f"outputs/subgraph_{song_id}",  # ← Con nombre de parámetro
            max_nodes=max_nodes  # ← AGREGADO
        )
        return {"status": "success", "file": f"outputs/subgraph_{song_id}.png"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/visualize/genres")
async def visualize_genre_network():
    """Genera red de conexiones entre géneros"""
    if not data_service.graph:
        raise HTTPException(status_code=400, detail="Grafo no construido")
    
    try:
        VisualizationService.generate_genre_network(
            data_service.graph,
            "outputs/genre_network"
        )
        return {"status": "success", "file": "outputs/genre_network.png"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))