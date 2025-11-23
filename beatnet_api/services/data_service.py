"""
Data Service - Carga datos y construye el grafo
"""
import json
from typing import List, Optional
from pathlib import Path
from models.song import Song
from models.graph import Graph
from core.similarity import build_graph_from_similarities

class DataService:
    """Servicio para manejar carga de datos y construcción del grafo"""
    
    def __init__(self, json_path: str = "data/songs.json"):
        self.json_path = json_path
        self.songs: List[Song] = []
        self.graph: Optional[Graph] = None
    
    def load_songs(self) -> List[Song]:
        """
        Carga canciones desde archivo JSON
        
        Returns:
            Lista de objetos Song
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.songs = [Song.from_dict(song_data) for song_data in data]
            print(f" Cargadas {len(self.songs)} canciones desde {self.json_path}")
            return self.songs
        
        except FileNotFoundError:
            print(f" Error: No se encontró el archivo {self.json_path}")
            return []
        except json.JSONDecodeError as e:
            print(f" Error al parsear JSON: {e}")
            return []
        except Exception as e:
            print(f" Error inesperado: {e}")
            return []
    
    def build_graph(self, min_similarity: float = 0.3, max_songs: Optional[int] = None) -> Graph:
        """
        Construye el grafo de similitudes entre canciones
        
        Args:
            min_similarity: Umbral mínimo de similitud para crear aristas
            max_songs: Limitar número de canciones (para testing)
        
        Returns:
            Grafo construido
        """
        if not self.songs:
            print("  No hay canciones cargadas. Llamando a load_songs()...")
            self.load_songs()
        
        songs_to_use = self.songs[:max_songs] if max_songs else self.songs
        
        print(f" Construyendo grafo con {len(songs_to_use)} canciones...")
        print(f"   Umbral de similitud: {min_similarity}")
        
        self.graph = build_graph_from_similarities(songs_to_use, min_similarity)
        
        stats = self.graph.get_statistics()
        print(f" Grafo construido:")
        print(f"   - Canciones: {stats['total_songs']}")
        print(f"   - Conexiones: {stats['total_connections']}")
        print(f"   - Grado promedio: {stats['average_degree']}")
        print(f"   - Densidad: {stats['density']}")
        
        return self.graph
    
    def get_song_by_id(self, song_id: str) -> Optional[Song]:
        """Busca canción por ID"""
        if self.graph:
            return self.graph.get_song(song_id)
        
        for song in self.songs:
            if song.id == song_id:
                return song
        return None
    
    def get_song_by_title(self, title: str, fuzzy: bool = True) -> Optional[Song]:
        """
        Busca canción por título
        
        Args:
            title: Título a buscar
            fuzzy: Si True, busca coincidencias parciales
        
        Returns:
            Primera canción que coincida
        """
        title_lower = title.lower()
        
        for song in self.songs:
            if fuzzy:
                if title_lower in song.title.lower():
                    return song
            else:
                if song.title.lower() == title_lower:
                    return song
        
        return None
    
    def get_songs_by_genre(self, genre: str) -> List[Song]:
        """Obtiene todas las canciones de un género"""
        genre_lower = genre.lower()
        return [s for s in self.songs if any(g.lower() == genre_lower for g in s.genres)]
    
    def get_songs_by_artist(self, artist: str, fuzzy: bool = True) -> List[Song]:
        """Obtiene canciones de un artista"""
        artist_lower = artist.lower()
        
        if fuzzy:
            return [s for s in self.songs if artist_lower in s.artist.lower()]
        else:
            return [s for s in self.songs if s.artist.lower() == artist_lower]
    
    def get_genre_statistics(self) -> dict:
        """Retorna estadísticas de géneros"""
        genre_count = {}
        
        for song in self.songs:
            for genre in song.genres:
                genre_count[genre] = genre_count.get(genre, 0) + 1
        
        # Ordenar por frecuencia
        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_genres": len(genre_count),
            "genres": dict(sorted_genres),
            "most_common": sorted_genres[:10] if sorted_genres else []
        }
    
    def get_artist_statistics(self) -> dict:
        """Retorna estadísticas de artistas"""
        artist_count = {}
        
        for song in self.songs:
            artist_count[song.artist] = artist_count.get(song.artist, 0) + 1
        
        sorted_artists = sorted(artist_count.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_artists": len(artist_count),
            "most_prolific": sorted_artists[:10]
        }
    
    def export_graph_data(self, output_path: str = "data/graph_export.json"):
        """Exporta datos del grafo a JSON"""
        if not self.graph:
            print(" No hay grafo construido")
            return
        
        export_data = {
            "statistics": self.graph.get_statistics(),
            "nodes": [],
            "edges": []
        }
        
        # Exportar nodos
        for song_id, node in self.graph.nodes.items():
            export_data["nodes"].append({
                "id": song_id,
                "title": node.song.title,
                "artist": node.song.artist,
                "genres": node.song.genres
            })
        
        # Exportar aristas (evitar duplicados)
        seen_edges = set()
        for song_id, node in self.graph.nodes.items():
            for neighbor_id, weight in node.neighbors.items():
                edge_key = tuple(sorted([song_id, neighbor_id]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    export_data["edges"].append({
                        "source": song_id,
                        "target": neighbor_id,
                        "weight": round(weight, 3)
                    })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f" Grafo exportado a {output_path}")

# import json
# from models.song import Song

# def load_and_clean_dataset(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         data = json.load(f)

#     songs = {}
#     for entry in data:
#         song_id = entry.get("id")
#         if not song_id or song_id in songs:
#             continue  # evitar duplicados

#         year = entry.get("year") if entry.get("year") is not None else "Unknown"
#         genres = [g.strip() for g in entry.get("genres", []) if g]

#         song = Song(
#             song_id=song_id,
#             title=entry.get("title", "Unknown"),
#             artist=entry.get("artist", "Unknown"),
#             genres=genres,
#             duration=entry.get("duration", 0),
#             year=year,
#             popularity=entry.get("popularity", 0),
#             preview_url=entry.get("preview_url", ""),
#             cover_url=entry.get("cover_url", "")
#         )
#         songs[song_id] = song

#     return list(songs.values())
