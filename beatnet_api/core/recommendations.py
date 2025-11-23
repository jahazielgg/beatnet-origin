"""
Algoritmos de Recomendación
Backtracking para encontrar secuencias óptimas de canciones
"""
from typing import List, Set, Tuple, Optional
from models.song import Song
from models.graph import Graph

def find_optimal_playlist(
    graph: Graph,
    start_song_id: str,
    playlist_length: int,
    min_similarity: float = 0.3
) -> Tuple[List[Song], float]:
    """
    BACKTRACKING OPTIMIZADO: Encuentra la secuencia óptima de canciones
    Busca la playlist con mayor similitud acumulada
    
    Args:
        graph: Grafo de canciones
        start_song_id: Canción inicial
        playlist_length: Longitud deseada de la playlist
        min_similarity: Similitud mínima entre canciones consecutivas
    
    Returns:
        Tupla (playlist, similitud_total)
    """
    if start_song_id not in graph.nodes or playlist_length < 1:
        return ([], 0.0)
    
    best_playlist = []
    best_score = 0.0
    iterations = [0]  # Contador de iteraciones
    MAX_ITERATIONS = 50000  # Límite para evitar timeouts
    
    def backtrack(current_path: List[str], current_score: float, visited: Set[str]):
        nonlocal best_playlist, best_score
        
        # Límite de iteraciones para evitar timeouts
        iterations[0] += 1
        if iterations[0] > MAX_ITERATIONS:
            return
        
        # Caso base: alcanzamos la longitud deseada
        if len(current_path) == playlist_length:
            if current_score > best_score:
                best_score = current_score
                best_playlist = [graph.get_song(sid) for sid in current_path]
            return
        
        # Obtener última canción del camino
        last_song_id = current_path[-1]
        node = graph.get_node(last_song_id)
        
        if not node:
            return
        
        # OPTIMIZACIÓN: Limitar vecinos a explorar (solo top 15)
        neighbors = sorted(node.neighbors.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for neighbor_id, similarity in neighbors:
            # Poda: si la similitud es muy baja, no explorar
            if similarity < min_similarity:
                continue
            
            # Evitar ciclos
            if neighbor_id in visited:
                continue
            
            # Poda optimista MEJORADA
            remaining_songs = playlist_length - len(current_path) - 1
            # Asumir que las siguientes canciones tendrán similitud del 80% del actual
            optimistic_score = current_score + similarity + (remaining_songs * similarity * 0.8)
            
            if optimistic_score <= best_score:
                continue
            
            # Explorar este camino
            current_path.append(neighbor_id)
            visited.add(neighbor_id)
            
            backtrack(current_path, current_score + similarity, visited)
            
            # Backtrack
            current_path.pop()
            visited.remove(neighbor_id)
    
    # Iniciar búsqueda
    backtrack([start_song_id], 0.0, {start_song_id})
    
    return (best_playlist, best_score)


def generate_diverse_playlist(
    graph: Graph,
    start_song_id: str,
    playlist_length: int,
    diversity_weight: float = 0.3
) -> List[Song]:
    """
    Genera playlist balanceando similitud y diversidad
    Usa backtracking con penalización por géneros repetidos
    
    Args:
        graph: Grafo de canciones
        start_song_id: Canción inicial
        playlist_length: Longitud de playlist
        diversity_weight: Peso de la diversidad (0 a 1)
    
    Returns:
        Playlist diversa
    """
    if start_song_id not in graph.nodes:
        return []
    
    playlist = [graph.get_song(start_song_id)]
    visited = {start_song_id}
    genre_count = {}
    
    # Contar géneros de la canción inicial
    start_song = graph.get_song(start_song_id)
    if start_song:
        for genre in start_song.genres:
            genre_count[genre] = genre_count.get(genre, 0) + 1
    
    current_id = start_song_id
    
    for _ in range(playlist_length - 1):
        node = graph.get_node(current_id)
        if not node or not node.neighbors:
            break
        
        best_candidate = None
        best_score = -1
        
        # Evaluar cada vecino
        for neighbor_id, similarity in node.neighbors.items():
            if neighbor_id in visited:
                continue
            
            neighbor_song = graph.get_song(neighbor_id)
            if not neighbor_song:
                continue
            
            # Calcular score de diversidad
            diversity_score = 0.0
            for genre in neighbor_song.genres:
                # Penalizar géneros ya usados
                penalty = genre_count.get(genre, 0) / len(playlist)
                diversity_score += (1 - penalty)
            
            diversity_score /= max(len(neighbor_song.genres), 1)
            
            # Score combinado
            combined_score = (1 - diversity_weight) * similarity + diversity_weight * diversity_score
            
            if combined_score > best_score:
                best_score = combined_score
                best_candidate = (neighbor_id, neighbor_song)
        
        if best_candidate:
            candidate_id, candidate_song = best_candidate
            playlist.append(candidate_song)
            visited.add(candidate_id)
            current_id = candidate_id
            
            # Actualizar conteo de géneros
            for genre in candidate_song.genres:
                genre_count[genre] = genre_count.get(genre, 0) + 1
        else:
            break
    
    return playlist


def find_all_playlists_with_constraints(
    graph: Graph,
    start_song_id: str,
    length: int,
    required_genres: Set[str] = None,
    max_results: int = 10
) -> List[Tuple[List[Song], float]]:
    """
    BACKTRACKING CON RESTRICCIONES: Encuentra todas las playlists que cumplan requisitos
    
    Args:
        graph: Grafo de canciones
        start_song_id: Canción inicial
        length: Longitud de playlist
        required_genres: Géneros que deben aparecer
        max_results: Máximo número de resultados
    
    Returns:
        Lista de (playlist, score) ordenadas por score
    """
    if start_song_id not in graph.nodes:
        return []
    
    results = []
    required_genres = required_genres or set()
    
    def has_all_genres(path_songs: List[Song]) -> bool:
        """Verifica si la playlist tiene todos los géneros requeridos"""
        if not required_genres:
            return True
        
        playlist_genres = set()
        for song in path_songs:
            playlist_genres.update(song.genres)
        
        return required_genres.issubset(playlist_genres)
    
    def backtrack(current_path: List[str], current_score: float, visited: Set[str]):
        # Limitar número de resultados
        if len(results) >= max_results:
            return
        
        # Caso base
        if len(current_path) == length:
            path_songs = [graph.get_song(sid) for sid in current_path]
            
            # Verificar restricciones
            if has_all_genres(path_songs):
                results.append((path_songs, current_score))
            return
        
        last_song_id = current_path[-1]
        node = graph.get_node(last_song_id)
        
        if not node:
            return
        
        for neighbor_id, similarity in node.neighbors.items():
            if neighbor_id not in visited:
                current_path.append(neighbor_id)
                visited.add(neighbor_id)
                
                backtrack(current_path, current_score + similarity, visited)
                
                current_path.pop()
                visited.remove(neighbor_id)
    
    backtrack([start_song_id], 0.0, {start_song_id})
    
    # Ordenar por score descendente
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:max_results]


def greedy_playlist(graph: Graph, start_song_id: str, length: int) -> List[Song]:
    """
    Algoritmo GREEDY (comparación): Siempre elige el vecino más similar
    Más rápido que backtracking pero no garantiza óptimo
    
    Args:
        graph: Grafo de canciones
        start_song_id: Canción inicial
        length: Longitud deseada
    
    Returns:
        Playlist generada con enfoque greedy
    """
    if start_song_id not in graph.nodes:
        return []
    
    playlist = [graph.get_song(start_song_id)]
    visited = {start_song_id}
    current_id = start_song_id
    
    for _ in range(length - 1):
        node = graph.get_node(current_id)
        if not node:
            break
        
        # Buscar vecino más similar no visitado
        best_neighbor = None
        best_similarity = -1
        
        for neighbor_id, similarity in node.neighbors.items():
            if neighbor_id not in visited and similarity > best_similarity:
                best_similarity = similarity
                best_neighbor = neighbor_id
        
        if best_neighbor:
            song = graph.get_song(best_neighbor)
            if song:
                playlist.append(song)
                visited.add(best_neighbor)
                current_id = best_neighbor
        else:
            break
    
    return playlist