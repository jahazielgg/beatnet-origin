"""
Song Model - Representa una canción en el sistema
"""
from typing import List, Optional
from dataclasses import dataclass
import requests 

@dataclass
class Song:
    """Modelo de canción con sus atributos"""
    id: str
    title: str
    artist: str
    genres: List[str]
    duration: int
    year: Optional[int]
    popularity: int
    preview_url: str
    cover_url: str
    deezer_id: Optional[str] = None
    _fresh_url_cache: Optional[str] = None  # No se serializa
    
    def __hash__(self):
        """Permite usar Song en sets y como keys en diccionarios"""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compara canciones por ID"""
        if not isinstance(other, Song):
            return False
        return self.id == other.id
    
    def similarity_score(self, other: 'Song') -> float:
        """
        Calcula similitud entre dos canciones (0.0 a 1.0)
        Basado en: géneros compartidos, diferencia de popularidad, año
        """
        if not isinstance(other, Song):
            return 0.0
        
        score = 0.0
        
        # Similitud de géneros (peso: 50%)
        if self.genres and other.genres:
            shared_genres = set(self.genres) & set(other.genres)
            total_genres = set(self.genres) | set(other.genres)
            genre_similarity = len(shared_genres) / len(total_genres) if total_genres else 0
            score += genre_similarity * 0.5
        
        # Similitud de popularidad (peso: 30%)
        max_pop = max(self.popularity, other.popularity)
        min_pop = min(self.popularity, other.popularity)
        if max_pop > 0:
            pop_similarity = min_pop / max_pop
            score += pop_similarity * 0.3
        
        # Similitud de año (peso: 20%)
        if self.year and other.year:
            year_diff = abs(self.year - other.year)
            year_similarity = max(0, 1 - (year_diff / 50))  # 50 años = 0% similar
            score += year_similarity * 0.2
        
        return score
    
    def to_dict(self):
        """Convierte a diccionario para JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genres": self.genres,
            "duration": self.duration,
            "year": self.year,
            "popularity": self.popularity,
            "preview_url": self.preview_url,
            "cover_url": self.cover_url,
            "deezer_id": self.deezer_id
        }
    
    def get_preview_url(self, force_refresh: bool = False) -> str:
        # Si no hay URL original, intentar regenerar
        if not self.preview_url or force_refresh:
            try:
                # Usar deezer_id si existe, sino usar id normal
                track_id = self.deezer_id or self.id
                
                url = f"https://api.deezer.com/track/{track_id}"
                response = requests.get(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    new_preview = data.get('preview', '')
                    
                    if new_preview:
                        self._fresh_url_cache = new_preview
                        return new_preview
            except:
                pass
            
        return self.preview_url
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Song':
        """Crea Song desde diccionario - Compatible con múltiples formatos"""

        # Convertir year si es string
        year = data.get("year")
        if year:
            if isinstance(year, str):
                try:
                    year = int(year) if year != "Unknown" else None
                except:
                    year = None

        # Seleccionar mejor cover disponible 
        cover_url = (
            data.get("cover_url") or       # Formato antiguo
            data.get("cover_xl") or         # Mejor calidad
            data.get("cover_big") or
            data.get("cover_medium") or
            data.get("cover_small") or
            ""
        )

        # Convertir deezer_id a string si viene como int
        deezer_id = data.get("deezer_id")
        if deezer_id:
            deezer_id = str(deezer_id)

        return cls(
            id=str(data["id"]),
            title=data["title"],
            artist=data["artist"],
            genres=data.get("genres", ["Unknown"]),
            duration=data.get("duration", 0),
            year=year,
            popularity=data.get("popularity", 0),
            preview_url=data.get("preview_url", ""),
            cover_url=cover_url,
            deezer_id=deezer_id  # NUEVO campo
        )
    
    def __repr__(self):
        return f"Song('{self.title}' by {self.artist})"