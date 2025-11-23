"""
Graph Model - Estructura de grafo para representar relaciones entre canciones
"""
from typing import Dict, List, Set, Optional, Tuple
from .song import Song

class Node:
    """Nodo del grafo que representa una canción"""
    def __init__(self, song: Song):
        self.song = song
        self.neighbors: Dict[str, float] = {}  # {song_id: similarity_weight}
    
    def add_neighbor(self, song_id: str, weight: float):
        """Agrega vecino con peso (similitud)"""
        self.neighbors[song_id] = weight
    
    def get_neighbors(self) -> List[Tuple[str, float]]:
        """Retorna lista de (song_id, weight) ordenados por peso DESC"""
        return sorted(self.neighbors.items(), key=lambda x: x[1], reverse=True)
    
    def __repr__(self):
        return f"Node({self.song.title}, neighbors={len(self.neighbors)})"


class Graph:
    """
    Grafo no dirigido ponderado de canciones
    Los pesos representan la similitud entre canciones (0.0 a 1.0)
    """
    def __init__(self):
        self.nodes: Dict[str, Node] = {}  # {song_id: Node}
    
    def add_song(self, song: Song):
        """Agrega una canción al grafo"""
        if song.id not in self.nodes:
            self.nodes[song.id] = Node(song)
    
    def add_edge(self, song_id1: str, song_id2: str, weight: float):
        """
        Agrega arista bidireccional entre dos canciones
        weight: similitud entre 0.0 y 1.0
        """
        if song_id1 in self.nodes and song_id2 in self.nodes:
            self.nodes[song_id1].add_neighbor(song_id2, weight)
            self.nodes[song_id2].add_neighbor(song_id1, weight)
    
    def get_song(self, song_id: str) -> Optional[Song]:
        """Obtiene canción por ID"""
        node = self.nodes.get(song_id)
        return node.song if node else None
    
    def get_node(self, song_id: str) -> Optional[Node]:
        """Obtiene nodo por ID de canción"""
        return self.nodes.get(song_id)
    
    def get_all_songs(self) -> List[Song]:
        """Retorna todas las canciones del grafo"""
        return [node.song for node in self.nodes.values()]
    
    def get_neighbors(self, song_id: str, min_similarity: float = 0.0) -> List[Tuple[Song, float]]:
        """
        Obtiene vecinos de una canción
        Returns: Lista de (Song, similarity) ordenados por similitud DESC
        """
        node = self.nodes.get(song_id)
        if not node:
            return []
        
        neighbors = []
        for neighbor_id, weight in node.get_neighbors():
            if weight >= min_similarity:
                neighbor_song = self.get_song(neighbor_id)
                if neighbor_song:
                    neighbors.append((neighbor_song, weight))
        
        return neighbors
    
    def get_edges_count(self) -> int:
        """Cuenta total de aristas (único)"""
        return sum(len(node.neighbors) for node in self.nodes.values()) // 2
    
    def get_statistics(self) -> dict:
        """Retorna estadísticas del grafo"""
        total_nodes = len(self.nodes)
        total_edges = self.get_edges_count()
        avg_degree = (total_edges * 2) / total_nodes if total_nodes > 0 else 0
        
        # Calcular densidad del grafo
        max_edges = (total_nodes * (total_nodes - 1)) / 2
        density = total_edges / max_edges if max_edges > 0 else 0
        
        return {
            "total_songs": total_nodes,
            "total_connections": total_edges,
            "average_degree": round(avg_degree, 2),
            "density": round(density, 4)
        }
    
    def __len__(self):
        return len(self.nodes)
    
    def __repr__(self):
        return f"Graph(songs={len(self.nodes)}, connections={self.get_edges_count()})"