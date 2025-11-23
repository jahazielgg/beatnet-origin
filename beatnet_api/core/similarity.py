"""
Algoritmos de Similitud entre Canciones
Incluye fuerza bruta O(n²) y optimizaciones
"""
from typing import List, Tuple
from models.song import Song
from models.graph import Graph

def brute_force_similarity(songs: List[Song], min_similarity: float = 0.3) -> List[Tuple[Song, Song, float]]:
    """
    FUERZA BRUTA O(n²): Compara todas las canciones entre sí
    
    Args:
        songs: Lista de canciones
        min_similarity: Umbral mínimo de similitud (0.0 a 1.0)
    
    Returns:
        Lista de tuplas (song1, song2, similarity_score)
    """
    results = []
    n = len(songs)
    
    for i in range(n):
        for j in range(i + 1, n):
            similarity = songs[i].similarity_score(songs[j])
            if similarity >= min_similarity:
                results.append((songs[i], songs[j], similarity))
    
    # Ordenar por similitud descendente
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def build_graph_from_similarities(songs: List[Song], min_similarity: float = 0.3) -> Graph:
    """
    Construye un grafo conectando canciones similares
    Usa fuerza bruta O(n²) para calcular todas las similitudes
    
    Args:
        songs: Lista de canciones
        min_similarity: Umbral mínimo para crear arista
    
    Returns:
        Grafo construido con aristas ponderadas por similitud
    """
    graph = Graph()
    
    # Agregar todos los nodos
    for song in songs:
        graph.add_song(song)
    
    # Calcular similitudes y crear aristas
    similarities = brute_force_similarity(songs, min_similarity)
    
    for song1, song2, weight in similarities:
        graph.add_edge(song1.id, song2.id, weight)
    
    return graph


def find_most_similar(target_song: Song, candidates: List[Song], top_k: int = 5) -> List[Tuple[Song, float]]:
    """
    Encuentra las k canciones más similares a una canción objetivo
    Complejidad: O(n log k) usando heap
    
    Args:
        target_song: Canción de referencia
        candidates: Lista de canciones candidatas
        top_k: Número de resultados a retornar
    
    Returns:
        Lista de (Song, similarity) ordenadas por similitud DESC
    """
    import heapq
    
    # Calcular similitudes
    similarities = []
    for candidate in candidates:
        if candidate.id != target_song.id:
            score = target_song.similarity_score(candidate)
            similarities.append((score, candidate))
    
    # Obtener top k usando heap (más eficiente que ordenar todo)
    top_k_items = heapq.nlargest(top_k, similarities, key=lambda x: x[0])
    
    # Retornar en formato (Song, score)
    return [(song, score) for score, song in top_k_items]


def find_similar_by_genre(target_song: Song, all_songs: List[Song], min_shared_genres: int = 1) -> List[Song]:
    """
    Optimización: Filtrado rápido por género O(n)
    Pre-filtra canciones antes de calcular similitud completa
    
    Args:
        target_song: Canción objetivo
        all_songs: Todas las canciones disponibles
        min_shared_genres: Mínimo de géneros compartidos
    
    Returns:
        Canciones que comparten al menos min_shared_genres géneros
    """
    target_genres = set(target_song.genres)
    similar_songs = []
    
    for song in all_songs:
        if song.id == target_song.id:
            continue
        
        shared = len(target_genres & set(song.genres))
        if shared >= min_shared_genres:
            similar_songs.append(song)
    
    return similar_songs


def batch_recommendations(songs: List[Song], batch_size: int = 10) -> dict:
    """
    DIVIDE Y CONQUISTA: Procesa canciones en lotes para recomendaciones
    Útil para datasets grandes
    
    Args:
        songs: Lista de canciones
        batch_size: Tamaño de cada lote
    
    Returns:
        Diccionario con estadísticas de procesamiento
    """
    total = len(songs)
    batches = [songs[i:i + batch_size] for i in range(0, total, batch_size)]
    
    results = {
        "total_songs": total,
        "total_batches": len(batches),
        "batch_size": batch_size,
        "batches_info": []
    }
    
    for idx, batch in enumerate(batches):
        batch_similarities = brute_force_similarity(batch, min_similarity=0.2)
        results["batches_info"].append({
            "batch_number": idx + 1,
            "songs_count": len(batch),
            "connections_found": len(batch_similarities)
        })
    
    return results