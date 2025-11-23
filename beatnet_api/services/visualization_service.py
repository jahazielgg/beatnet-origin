"""
Visualization Service - Genera gráficos con Graphviz
"""
import graphviz as gv
from typing import List, Optional, Set
from models.graph import Graph
from models.song import Song

class VisualizationService:
    """Servicio para generar visualizaciones del grafo"""
    
    @staticmethod
    def generate_full_graph(
        graph: Graph,
        output_path: str = "outputs/full_graph",
        max_nodes: int = 50,
        min_similarity: float = 0.4
    ):
        """
        Genera visualización completa del grafo
        
        Args:
            graph: Grafo a visualizar
            output_path: Ruta de salida (sin extensión)
            max_nodes: Máximo de nodos a mostrar
            min_similarity: Similitud mínima para mostrar arista
        """
        dot = gv.Graph(comment='Music Recommendation Graph', engine='neato')
        dot.attr(
            bgcolor='#1a1a2e',
            fontcolor='white',
            splines='true',
            overlap='false'
        )
        
        # Tomar subset de nodos si es muy grande
        nodes_to_show = list(graph.nodes.items())[:max_nodes]
        node_ids = {song_id for song_id, _ in nodes_to_show}
        
        # Agregar nodos
        for song_id, node in nodes_to_show:
            song = node.song
            
            # Color basado en género principal
            color = VisualizationService._get_genre_color(song.genres[0] if song.genres else "Unknown")
            
            # Tamaño basado en popularidad
            size = max(0.3, min(2.0, song.popularity / 500000))
            
            dot.node(
                song_id,
                label=f"{song.title}\n{song.artist}",
                shape='circle',
                style='filled',
                fillcolor=color,
                fontcolor='white',
                fontsize='10',
                width=str(size),
                height=str(size)
            )
        
        # Agregar aristas
        seen_edges = set()
        for song_id, node in nodes_to_show:
            for neighbor_id, weight in node.neighbors.items():
                if neighbor_id not in node_ids:
                    continue
                
                if weight < min_similarity:
                    continue
                
                edge_key = tuple(sorted([song_id, neighbor_id]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    
                    # Grosor y color basado en similitud
                    penwidth = str(weight * 3)
                    opacity = int(weight * 255)
                    color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
                    
                    dot.edge(
                        song_id,
                        neighbor_id,
                        penwidth=penwidth,
                        color=color
                    )
        
        # Renderizar
        dot.render(output_path, format='png', cleanup=True)
        print(f" Grafo guardado en {output_path}.png")
    
    @staticmethod
    def generate_subgraph(
        graph: Graph,
        center_song_id: str,
        depth: int = 2,
        output_path: str = "outputs/subgraph",
        max_nodes: int = 30  # NUEVO: Limitar nodos
    ):
        """
        Genera subgrafo centrado en una canción
        
        Args:
            graph: Grafo completo
            center_song_id: ID de canción central
            depth: Profundidad de vecindad a incluir
            output_path: Ruta de salida
            max_nodes: Máximo número de nodos a incluir
        """
        from collections import deque
        
        center_song = graph.get_song(center_song_id)
        if not center_song:
            print(f" Canción {center_song_id} no encontrada")
            return
        
        # BFS para obtener vecindad CON LÍMITE
        visited = set()
        queue = deque([(center_song_id, 0)])
        subgraph_nodes = []  # Lista ordenada por profundidad
        
        while queue and len(subgraph_nodes) < max_nodes:
            current_id, current_depth = queue.popleft()
            
            if current_id in visited or current_depth > depth:
                continue
            
            visited.add(current_id)
            subgraph_nodes.append(current_id)
            
            if current_depth < depth:
                node = graph.get_node(current_id)
                if node:
                    # Ordenar vecinos por similitud (tomar solo los mejores)
                    neighbors_sorted = sorted(
                        node.neighbors.items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:10]  # Solo top 10 vecinos por nodo
                    
                    for neighbor_id, _ in neighbors_sorted:
                        if neighbor_id not in visited and len(subgraph_nodes) < max_nodes:
                            queue.append((neighbor_id, current_depth + 1))
        
        subgraph_nodes_set = set(subgraph_nodes)
        
        # Crear grafo - OPTIMIZADO
        dot = gv.Digraph(comment=f'Subgraph: {center_song.title}', engine='dot')
        dot.attr(rankdir='TB', bgcolor='#0f0f1e', fontcolor='white')
        
        # Agregar nodos
        for song_id in subgraph_nodes[:max_nodes]:  # Asegurar límite
            node = graph.get_node(song_id)
            if not node:
                continue
            
            song = node.song
            is_center = (song_id == center_song_id)
            
            # Truncar títulos largos para mejor visualización
            title_display = song.title[:30] + "..." if len(song.title) > 30 else song.title
            artist_display = song.artist[:20] + "..." if len(song.artist) > 20 else song.artist
            
            color = '#ff6b6b' if is_center else VisualizationService._get_genre_color(
                song.genres[0] if song.genres else "Unknown"
            )
            
            dot.node(
                song_id,
                label=f"{title_display}\n{artist_display}",
                shape='box' if is_center else 'ellipse',
                style='filled',
                fillcolor=color,
                fontcolor='white',
                fontsize='12' if is_center else '10'
            )
        
        # Agregar aristas - SOLO las más importantes
        edges_added = 0
        max_edges = 50  # Límite de aristas para evitar sobrecarga
        
        for song_id in subgraph_nodes[:max_nodes]:
            if edges_added >= max_edges:
                break
                
            node = graph.get_node(song_id)
            if not node:
                continue
            
            neighbors_sorted = sorted(node.neighbors.items(), key=lambda x: x[1], reverse=True)
            
            for neighbor_id, weight in neighbors_sorted[:3]:  # Solo top 3 vecinos por nodo
                if neighbor_id in subgraph_nodes_set and edges_added < max_edges:
                    dot.edge(
                        song_id,
                        neighbor_id,
                        label=f"{weight:.2f}",
                        fontsize='8',
                        color='white'
                    )
                    edges_added += 1
        
        dot.render(output_path, format='png', cleanup=True)
        print(f" Subgrafo guardado en {output_path}.png ({len(subgraph_nodes)} nodos, {edges_added} aristas)")
   
    @staticmethod
    def generate_playlist_visualization(
        playlist: List[Song],
        similarities: List[float],
        output_path: str = "outputs/playlist"
    ):
        """
        Visualiza una playlist como secuencia lineal
        
        Args:
            playlist: Lista de canciones en orden
            similarities: Similitudes entre canciones consecutivas
            output_path: Ruta de salida
        """
        dot = gv.Digraph(comment='Playlist', engine='dot')
        dot.attr(rankdir='LR', bgcolor='#16213e', fontcolor='white')
        
        for i, song in enumerate(playlist):
            color = VisualizationService._get_genre_color(song.genres[0] if song.genres else "Unknown")
            
            dot.node(
                str(i),
                label=f"{i+1}. {song.title}\n{song.artist}\n{'⭐' * min(5, int(song.popularity / 200000))}",
                shape='box',
                style='filled,rounded',
                fillcolor=color,
                fontcolor='white',
                fontsize='11'
            )
            
            if i < len(playlist) - 1 and i < len(similarities):
                similarity = similarities[i]
                penwidth = str(similarity * 4)
                label = f"{similarity:.2f}"
                
                dot.edge(
                    str(i),
                    str(i + 1),
                    label=label,
                    penwidth=penwidth,
                    color='#4ecca3',
                    fontcolor='white',
                    fontsize='10'
                )
        
        dot.render(output_path, format='png', cleanup=True)
        print(f" Playlist visualizada en {output_path}.png")
    
    @staticmethod
    def generate_genre_network(
        graph: Graph,
        output_path: str = "outputs/genre_network"
    ):
        """
        Genera red de géneros musicales
        Nodos = géneros, Aristas = canciones compartidas
        """
        genre_connections = {}
        genre_songs = {}
        
        # Construir red de géneros
        for node in graph.nodes.values():
            song = node.song
            for genre in song.genres:
                if genre not in genre_songs:
                    genre_songs[genre] = []
                genre_songs[genre].append(song)
        
        # Calcular conexiones entre géneros
        for genre1 in genre_songs:
            for genre2 in genre_songs:
                if genre1 >= genre2:
                    continue
                
                # Contar canciones compartidas entre géneros
                shared_count = 0
                for song in genre_songs[genre1]:
                    if any(g == genre2 for g in song.genres):
                        shared_count += 1
                
                if shared_count > 0:
                    genre_connections[(genre1, genre2)] = shared_count
        
        # Crear grafo
        dot = gv.Graph(comment='Genre Network', engine='fdp')
        dot.attr(bgcolor='#1a1a2e', fontcolor='white', overlap='false')
        
        # Agregar nodos (géneros)
        for genre, songs in genre_songs.items():
            size = max(0.5, min(3.0, len(songs) / 20))
            color = VisualizationService._get_genre_color(genre)
            
            dot.node(
                genre,
                label=f"{genre}\n({len(songs)})",
                shape='circle',
                style='filled',
                fillcolor=color,
                fontcolor='white',
                fontsize='12',
                width=str(size),
                height=str(size)
            )
        
        # Agregar aristas
        for (genre1, genre2), count in genre_connections.items():
            if count >= 3:  # Mostrar solo conexiones significativas
                penwidth = str(min(5, count / 5))
                dot.edge(genre1, genre2, penwidth=penwidth, color='#4ecca3')
        
        dot.render(output_path, format='png', cleanup=True)
        print(f" Red de géneros guardada en {output_path}.png")
    
    @staticmethod
    def _get_genre_color(genre: str) -> str:
        """Retorna color hexadecimal según género"""
        colors = {
            "Pop": "#e91e63",
            "Rock": "#f44336",
            "Hip Hop": "#9c27b0",
            "Electronic": "#3f51b5",
            "Jazz": "#00bcd4",
            "Classical": "#009688",
            "R&B": "#4caf50",
            "Country": "#ff9800",
            "Reggae": "#ff5722",
            "Metal": "#795548"
        }
        return colors.get(genre, "#607d8b")