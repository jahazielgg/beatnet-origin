"""
Algoritmos de Búsqueda en Grafos
BFS, DFS, Dijkstra para encontrar caminos y conexiones
"""
from typing import List, Optional, Dict, Set, Tuple
from collections import deque
import heapq
from models.graph import Graph
from models.song import Song

def bfs_search(graph: Graph, start_song_id: str, max_depth: int = 3) -> List[Song]:
    """
    BFS (Breadth-First Search) - Búsqueda en Amplitud
    Encuentra canciones conectadas hasta cierta profundidad
    
    Args:
        graph: Grafo de canciones
        start_song_id: ID de canción inicial
        max_depth: Profundidad máxima de búsqueda
    
    Returns:
        Lista de canciones alcanzables ordenadas por cercanía
    """
    if start_song_id not in graph.nodes:
        return []
    
    visited = set()
    queue = deque([(start_song_id, 0)])  # (song_id, depth)
    result = []
    
    while queue:
        current_id, depth = queue.popleft()
        
        if current_id in visited or depth > max_depth:
            continue
        
        visited.add(current_id)
        current_song = graph.get_song(current_id)
        
        if current_song and current_id != start_song_id:
            result.append(current_song)
        
        # Agregar vecinos a la cola
        node = graph.get_node(current_id)
        if node and depth < max_depth:
            for neighbor_id, _ in node.neighbors.items():
                if neighbor_id not in visited:
                    queue.append((neighbor_id, depth + 1))
    
    return result


def dfs_search(graph: Graph, start_song_id: str, max_depth: int = 3) -> List[Song]:
    """
    DFS (Depth-First Search) - Búsqueda en Profundidad
    Explora caminos completos antes de retroceder
    
    Args:
        graph: Grafo de canciones
        start_song_id: ID de canción inicial
        max_depth: Profundidad máxima
    
    Returns:
        Lista de canciones encontradas en orden DFS
    """
    if start_song_id not in graph.nodes:
        return []
    
    visited = set()
    result = []
    
    def dfs_recursive(song_id: str, depth: int):
        if song_id in visited or depth > max_depth:
            return
        
        visited.add(song_id)
        current_song = graph.get_song(song_id)
        
        if current_song and song_id != start_song_id:
            result.append(current_song)
        
        # Visitar vecinos
        node = graph.get_node(song_id)
        if node and depth < max_depth:
            # Ordenar vecinos por peso para explorar primero los más similares
            neighbors_sorted = sorted(node.neighbors.items(), key=lambda x: x[1], reverse=True)
            for neighbor_id, _ in neighbors_sorted:
                if neighbor_id not in visited:
                    dfs_recursive(neighbor_id, depth + 1)
    
    dfs_recursive(start_song_id, 0)
    return result


def dijkstra_shortest_path(graph: Graph, start_song_id: str, end_song_id: str) -> Optional[Tuple[List[Song], float]]:
    """
    Algoritmo de Dijkstra - Camino más corto
    Encuentra el camino con mayor similitud acumulada (peso invertido)
    
    Args:
        graph: Grafo de canciones
        start_song_id: Canción inicial
        end_song_id: Canción objetivo
    
    Returns:
        Tupla (camino, similitud_total) o None si no hay camino
    """
    if start_song_id not in graph.nodes or end_song_id not in graph.nodes:
        return None
    
    # Caso especial: mismo nodo
    if start_song_id == end_song_id:
        song = graph.get_song(start_song_id)
        return ([song], 0.0) if song else None
    
    # Usamos similitud negativa como distancia (mayor similitud = menor distancia)
    distances = {song_id: float('inf') for song_id in graph.nodes}
    distances[start_song_id] = 0
    
    previous = {}
    visited = set()
    
    # Priority queue: (distancia, song_id)
    pq = [(0, start_song_id)]
    
    while pq:
        current_dist, current_id = heapq.heappop(pq)
        
        if current_id in visited:
            continue
        
        visited.add(current_id)
        
        if current_id == end_song_id:
            break
        
        node = graph.get_node(current_id)
        if not node:
            continue
        
        for neighbor_id, weight in node.neighbors.items():
            if neighbor_id in visited:
                continue
            
            # Usamos (1 - weight) como distancia
            distance = current_dist + (1 - weight)
            
            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                previous[neighbor_id] = current_id
                heapq.heappush(pq, (distance, neighbor_id))
    
    # Reconstruir camino
    if end_song_id not in previous and start_song_id != end_song_id:
        return None
    
    path = []
    current = end_song_id
    
    while current != start_song_id:
        song = graph.get_song(current)
        if song:
            path.append(song)
        
        if current not in previous:
            break
        current = previous[current]
    
    # Agregar canción inicial
    start_song = graph.get_song(start_song_id)
    if start_song:
        path.append(start_song)
    
    path.reverse()
    
    # CORRECCIÓN: Calcular similitud real del camino
    total_similarity = 0.0
    for i in range(len(path) - 1):
        sim = path[i].similarity_score(path[i + 1])
        total_similarity += sim
    
    return (path, total_similarity)

def find_connected_components(graph: Graph) -> List[List[Song]]:
    """
    Encuentra componentes conexas del grafo usando BFS
    Útil para identificar clusters de canciones relacionadas
    
    Returns:
        Lista de componentes (cada componente es una lista de canciones)
    """
    visited = set()
    components = []
    
    for song_id in graph.nodes:
        if song_id not in visited:
            # Nueva componente
            component = []
            queue = deque([song_id])
            
            while queue:
                current_id = queue.popleft()
                
                if current_id in visited:
                    continue
                
                visited.add(current_id)
                song = graph.get_song(current_id)
                if song:
                    component.append(song)
                
                # Agregar vecinos
                node = graph.get_node(current_id)
                if node:
                    for neighbor_id in node.neighbors:
                        if neighbor_id not in visited:
                            queue.append(neighbor_id)
            
            if component:
                components.append(component)
    
    # Ordenar componentes por tamaño (mayor a menor)
    components.sort(key=len, reverse=True)
    return components