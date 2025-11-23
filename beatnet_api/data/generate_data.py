import requests
import json
import time
from typing import List, Dict

def obtener_canciones_por_genero(genre_id, genre_name, limit=100):
    """Obtiene canciones populares de un género específico"""
    url = f"https://api.deezer.com/genre/{genre_id}/artists"
    response = requests.get(url)
    
    canciones = []
    if response.status_code == 200:
        artistas = response.json().get('data', [])[:20]
        
        for artista in artistas:
            tracks_url = f"https://api.deezer.com/artist/{artista['id']}/top?limit=5"
            tracks_response = requests.get(tracks_url)
            
            if tracks_response.status_code == 200:
                tracks = tracks_response.json().get('data', [])
                # Asignar el género al track desde el inicio
                for track in tracks:
                    track['_genre_asignado'] = genre_name
                canciones.extend(tracks)
                
                if len(canciones) >= limit:
                    break
            
            time.sleep(0.3)
    
    return canciones[:limit]

def obtener_chart_global(limit=100):
    """Obtiene las canciones del chart global"""
    url = "https://api.deezer.com/chart/0/tracks"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('data', [])[:limit]
    return []

def buscar_por_palabra_clave(keyword, limit=50):
    """Busca canciones por palabra clave"""
    url = f"https://api.deezer.com/search?q={keyword}&limit={limit}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('data', [])
    return []

def detectar_genero_por_artista(artist_name):
    """Detecta género basándose en el nombre del artista usando búsqueda"""
    url = f"https://api.deezer.com/search/artist?q={artist_name}&limit=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            artist_id = data[0]['id']
            # Intentar obtener info del artista
            artist_url = f"https://api.deezer.com/artist/{artist_id}"
            artist_response = requests.get(artist_url)
            if artist_response.status_code == 200:
                artist_info = artist_response.json()
                # Intentar obtener radio del artista que tiene mejor info de géneros
                if 'tracklist' in artist_info:
                    return None
    return None

def inferir_genero_por_popularidad(track_data):
    """Infiere género basándose en características de la canción"""
    rank = track_data.get('rank', 0)
    
    # Si está en top charts, probablemente sea Pop
    if rank > 800000:
        return "Pop"
    elif rank > 500000:
        return "Dance"
    else:
        return "Pop"

def procesar_cancion(track_data, genero_contextual=None):
    """Convierte datos de Deezer al formato de nuestro dataset"""
    
    # SOLUCIÓN AL PROBLEMA DE GÉNEROS:
    # 1. Usar el género contextual si se pasó (cuando viene de búsqueda por género)
    # 2. Si no, intentar usar el album/artista
    # 3. Como último recurso, usar "Pop"
    
    generos = []
    
    # Prioridad 1: Género asignado contextualmente
    if '_genre_asignado' in track_data:
        generos = [track_data['_genre_asignado']]
    elif genero_contextual:
        generos = [genero_contextual]
    else:
        # Prioridad 2: Inferir del rank/popularidad
        genero_inferido = inferir_genero_por_popularidad(track_data)
        generos = [genero_inferido]
    
    # SOLUCIÓN AL PROBLEMA DE URLs:
    # En lugar de guardar solo el preview_url temporal, guardamos múltiples formas de acceder
    
    track_id = track_data['id']
    
    return {
        "id": str(track_id),
        "title": track_data['title'],
        "artist": track_data['artist']['name'],
        "album": track_data.get('album', {}).get('title', 'Unknown'),
        "genres": generos,
        "duration": track_data['duration'],
        "year": track_data.get('release_date', 'Unknown')[:4] if track_data.get('release_date') else None,
        "popularity": track_data.get('rank', 0),
        
        # MÚLTIPLES FORMAS DE ACCEDER AL AUDIO:
        "deezer_id": track_id,  # Para reconstruir URLs después
        "deezer_link": track_data.get('link', f"https://www.deezer.com/track/{track_id}"),
        "preview_url": track_data.get('preview', ''),  # Este expira pero lo guardamos igual
        
        # URLs de imágenes (también pueden expirar pero menos común)
        "cover_small": track_data.get('album', {}).get('cover_small', ''),
        "cover_medium": track_data.get('album', {}).get('cover_medium', ''),
        "cover_big": track_data.get('album', {}).get('cover_big', ''),
        "cover_xl": track_data.get('album', {}).get('cover_xl', '')
    }

def generar_dataset_masivo(objetivo=2000, nombre_archivo="canciones.json"):
    """
    Genera un dataset grande y variado de canciones
    """
    print(f"Generando dataset de {objetivo} canciones variadas...\n")
    
    dataset = []
    ids_vistos = set()
    
    # Géneros de Deezer con mejor mapeo
    GENEROS = {
        132: "Pop",
        116: "Hip Hop", 
        152: "Rock",
        113: "Dance",
        165: "R&B",
        85: "Alternative",
        106: "Electro",
        144: "Reggae",
        129: "Jazz",
        98: "Classical",
        464: "Indie Pop",
        173: "Soundtrack",
        169: "Latin",
        466: "Folk",
        153: "Metal",
        84: "Country"
    }
    
    # 1. Chart global (estos serán mayormente Pop)
    print("[1/4] Obteniendo chart global...")
    chart_tracks = obtener_chart_global(100)
    print(f"  → {len(chart_tracks)} canciones del chart")
    
    for track in chart_tracks:
        if track['id'] not in ids_vistos and track.get('preview'):
            try:
                cancion = procesar_cancion(track, genero_contextual="Pop")
                dataset.append(cancion)
                ids_vistos.add(track['id'])
            except Exception as e:
                print(f"    Error procesando track: {e}")
    
    print(f"    Total acumulado: {len(dataset)}\n")
    time.sleep(1)
    
    # 2. Canciones por género (AQUÍ SE ARREGLA EL PROBLEMA)
    print("[2/4] Obteniendo canciones por género...")
    canciones_por_genero = max(10, (objetivo - len(dataset)) // len(GENEROS))
    
    for genre_id, genre_name in GENEROS.items():
        if len(dataset) >= objetivo:
            break
            
        print(f"  → Procesando género: {genre_name}")
        tracks = obtener_canciones_por_genero(genre_id, genre_name, canciones_por_genero)
        
        agregadas = 0
        for track in tracks:
            if len(dataset) >= objetivo:
                break
            if track['id'] not in ids_vistos and track.get('preview'):
                try:
                    # El género ya viene en track['_genre_asignado']
                    cancion = procesar_cancion(track)
                    dataset.append(cancion)
                    ids_vistos.add(track['id'])
                    agregadas += 1
                except Exception as e:
                    print(f"    Error: {e}")
        
        print(f"    ✓ Agregadas: {agregadas} | Total: {len(dataset)}")
        time.sleep(0.5)
    
    print(f"\n  ✓ Total acumulado: {len(dataset)}\n")
    
    # 3. Búsquedas por palabras clave
    print("[3/4] Completando con búsquedas variadas...")
    KEYWORDS = [
        "love", "night", "summer", "fire", "dreams", "heart", "star", 
        "dance", "party", "feel", "time", "life", "world", "soul",
        "baby", "girl", "boy", "way", "light", "dark", "electric",
        "sweet", "crazy", "wild", "free", "beautiful", "forever"
    ]
    
    for keyword in KEYWORDS:
        if len(dataset) >= objetivo:
            break
        
        tracks = buscar_por_palabra_clave(keyword, 50)
        agregadas = 0
        
        for track in tracks:
            if len(dataset) >= objetivo:
                break
            if track['id'] not in ids_vistos and track.get('preview'):
                try:
                    cancion = procesar_cancion(track, genero_contextual="Pop")
                    dataset.append(cancion)
                    ids_vistos.add(track['id'])
                    agregadas += 1
                except:
                    pass
        
        if agregadas > 0:
            print(f"  → '{keyword}': +{agregadas} canciones | Total: {len(dataset)}")
        time.sleep(0.3)
    
    print(f"\n  ✓ Total acumulado: {len(dataset)}\n")
    
    # 4. Guardar dataset
    print("[4/4] Guardando dataset...")
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    
    # Estadísticas finales
    print(f"\n{'='*60}")
    print(f"DATASET GENERADO: {nombre_archivo}")
    print(f"{'='*60}")
    print(f"Total de canciones: {len(dataset)}")
    
    todos_generos = {}
    todos_artistas = set()
    for cancion in dataset:
        todos_artistas.add(cancion['artist'])
        for genero in cancion['genres']:
            todos_generos[genero] = todos_generos.get(genero, 0) + 1
    
    print(f"Artistas únicos: {len(todos_artistas)}")
    print(f"Géneros únicos: {len(todos_generos)}")
    print(f"\nDistribución de géneros:")
    top_generos = sorted(todos_generos.items(), key=lambda x: x[1], reverse=True)
    for genero, count in top_generos:
        porcentaje = (count / len(dataset)) * 100
        print(f"  - {genero}: {count} canciones ({porcentaje:.1f}%)")
    
    print(f"\n  NOTA SOBRE URLs:")
    print(f"  - Los preview_url pueden expirar en horas/días")
    print(f"  - Usa 'deezer_id' para reconstruir URLs dinámicamente:")
    print(f"    • Preview: https://cdns-preview-X.dzcdn.net/stream/c-TRACKID...")
    print(f"    • Link web: https://www.deezer.com/track/TRACKID")
    print(f"  - Considera usar la API en tiempo real para obtener previews frescos")
    
    return dataset

def regenerar_preview_url(track_id):
    """
    Función helper para regenerar URLs de preview cuando expiren
    """
    url = f"https://api.deezer.com/track/{track_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('preview', None)
    return None

if __name__ == "__main__":
    print(" GENERADOR DE DATASET MASIVO - DEEZER API \n")
    
    # Generar dataset de 2000 canciones
    dataset = generar_dataset_masivo(objetivo=2000, nombre_archivo="new_songs.json")
    
    print(f"\n  ¡Proceso completado!")
    print(f"    Archivo: new_songs.json")
    print(f"\n  Para regenerar un preview URL cuando expire:")
    print(f"   preview = regenerar_preview_url(track_id)")