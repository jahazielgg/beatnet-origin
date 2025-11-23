"""
Script de prueba local - Optimizado para datasets grandes
"""
from services.data_service import DataService
from services.visualization_service import VisualizationService
from core.similarity import find_most_similar
from core.search import bfs_search, dfs_search, dijkstra_shortest_path
from core.sorting import merge_sort, quick_sort, get_top_k_songs
from core.recommendations import find_optimal_playlist, generate_diverse_playlist, greedy_playlist
from models.graph import Graph
import threading

class TimeoutException(Exception):
    pass

def test_all():
    print("=" * 60)
    print("TESTING BEATNET SYSTEM (2000 CANCIONES)")
    print("=" * 60)
    
    # 1. CARGAR DATOS
    print("\n[1] Cargando datos...")
    service = DataService("data/songs.json")
    songs = service.load_songs()
    
    if not songs:
        print("ERROR: No se pudieron cargar canciones")
        return
    
    print(f"Cargadas {len(songs)} canciones")
    
    # 2. CONSTRUIR GRAFO COMPLETO (2000 canciones)
    print("\n[2] Construyendo grafo completo...")
    print("    (Esto puede tomar 1-2 minutos con 2000 canciones...)")
    
    graph = service.build_graph(
        min_similarity=0.3,  # Ajusta según prefieras
        max_songs=None       # SIN límite - usar todas las canciones
    )
    
    # 3. ESTADÍSTICAS
    print("\n[3] Estadísticas del sistema:")
    stats = graph.get_statistics()
    print(f"    Canciones: {stats['total_songs']}")
    print(f"    Conexiones: {stats['total_connections']}")
    print(f"    Grado promedio: {stats['average_degree']:.2f}")
    print(f"    Densidad: {stats['density']:.6f}")

    genre_stats = service.get_genre_statistics()
    print(f"\n    Total de géneros: {genre_stats['total_genres']}")
    print(f"    Géneros más populares:")
    for genre, count in genre_stats['most_common'][:5]:
        print(f"      - {genre}: {count} canciones")
    
    # 4. PRUEBA DE ORDENAMIENTO (usar todas las canciones)
    print("\n[4] Probando algoritmos de ordenamiento...")
    
    # MergeSort - muestra reducida
    print("    MergeSort por popularidad (muestra de 50)...")
    sorted_merge = merge_sort(songs[:50], key=lambda s: s.popularity, reverse=True)
    print(f"      Top 3: {sorted_merge[0].title}, {sorted_merge[1].title}, {sorted_merge[2].title}")
    
    # QuickSort - muestra reducida
    print("    QuickSort por título (muestra de 50)...")
    sorted_quick = quick_sort(songs[:50], key=lambda s: s.title)
    print(f"      Primeros 3: {sorted_quick[0].title}, {sorted_quick[1].title}, {sorted_quick[2].title}")
    
    # QuickSelect - Top K sobre TODAS las canciones
    print(f"    QuickSelect - Top 10 más populares (de {len(songs)} canciones)...")
    top_10 = get_top_k_songs(songs, 10, key=lambda s: s.popularity)
    for i, song in enumerate(top_10, 1):
        print(f"      {i}. {song.title} - {song.artist} ({song.popularity:,})")
    
    # 5. PRUEBA DE BÚSQUEDA (usar grafo completo)
    print("\n[5] Probando algoritmos de búsqueda...")
    test_song = list(graph.nodes.values())[0].song
    print(f"    Canción de prueba: '{test_song.title}' por {test_song.artist}")
    
    # BFS
    print("    BFS (profundidad 3)...")
    bfs_results = bfs_search(graph, test_song.id, max_depth=3)
    print(f"      Encontradas {len(bfs_results)} canciones")
    if bfs_results:
        print(f"      Ejemplos: {', '.join([s.title for s in bfs_results[:3]])}")
    
    # DFS
    print("    DFS (profundidad 3)...")
    dfs_results = dfs_search(graph, test_song.id, max_depth=3)
    print(f"      Encontradas {len(dfs_results)} canciones")
    
    # Dijkstra
    if len(graph.nodes) >= 2:
        song_ids = list(graph.nodes.keys())
        start_id = song_ids[0]
        end_id = song_ids[min(10, len(song_ids) - 1)]
        
        print(f"    Dijkstra - Camino más corto...")
        path_result = dijkstra_shortest_path(graph, start_id, end_id)
        
        if path_result:
            path, similarity = path_result
            print(f"      Camino encontrado: {len(path)} canciones")
            print(f"      Similitud total: {similarity:.3f}")
            print(f"      Ruta: {' → '.join([s.title for s in path[:4]])}...")
        else:
            print("      No se encontró camino")
    
    # 6. RECOMENDACIONES (usar grafo completo)
    print("\n[6] Probando sistema de recomendaciones...")
    
    print("    Top 10 recomendaciones por similitud...")
    recommendations = find_most_similar(test_song, graph.get_all_songs(), top_k=10)
    for i, (rec_song, similarity) in enumerate(recommendations, 1):
        print(f"      {i}. {rec_song.title} - {rec_song.artist} (sim: {similarity:.3f})")
    
    # 7. PLAYLISTS - AQUI ESTA LA CLAVE
    print("\n[7] Generando playlists...")
    print("    Usando subgrafo optimizado para algoritmos pesados...")
    
    # CREAR SUBGRAFO PEQUEÑO SOLO PARA PLAYLISTS
    # Obtener canciones cercanas usando BFS
    nearby_songs = bfs_search(graph, test_song.id, max_depth=2)
    
    # Limitar a las 100 más similares a la canción inicial
    nearby_with_sim = [(s, test_song.similarity_score(s)) for s in nearby_songs]
    nearby_with_sim.sort(key=lambda x: x[1], reverse=True)
    top_nearby = [s for s, _ in nearby_with_sim[:100]]
    
    print(f"    Subgrafo creado: {len(top_nearby)} canciones cercanas")
    
    # Crear grafo temporal pequeño
    small_graph = Graph()
    
    # Agregar nodos usando add_song
    for song in top_nearby:
        small_graph.add_song(song)
    
    # Agregar conexiones
    for i, song1 in enumerate(top_nearby):
        for song2 in top_nearby[i+1:]:
            similarity = song1.similarity_score(song2)
            if similarity >= 0.3:  # Mismo threshold
                small_graph.add_edge(song1.id, song2.id, similarity)
    
    print(f"    Conexiones en subgrafo: {small_graph.get_edges_count()}")
    
    # GREEDY (rápido incluso con grafo grande)
    print("\n    [7.1] Playlist GREEDY (algoritmo voraz)...")
    try:
        greedy_pl = greedy_playlist(graph, test_song.id, length=8)
        if greedy_pl:
            print(f"      Generada: {len(greedy_pl)} canciones")
            for i, song in enumerate(greedy_pl, 1):
                print(f"      {i}. {song.title} - {song.artist}")
            
            # Calcular similitud
            if len(greedy_pl) > 1:
                total_sim = sum(greedy_pl[i].similarity_score(greedy_pl[i+1]) 
                               for i in range(len(greedy_pl)-1))
                print(f"      Similitud promedio: {total_sim/(len(greedy_pl)-1):.3f}")
    except Exception as e:
        print(f"      ERROR: {e}")
    
    # BACKTRACKING (usar subgrafo pequeño)
    print("\n    [7.2] Playlist OPTIMA (backtracking en subgrafo)...")
    print("          Timeout: 30 segundos")
    
    optimal_pl = None
    optimal_sim = 0
    result_container = [None, None]  # Para almacenar resultado del thread
    
    def run_backtracking():
        try:
            pl, sim = find_optimal_playlist(
                small_graph,
                test_song.id, 
                playlist_length=5,
                min_similarity=0.4
            )
            result_container[0] = pl
            result_container[1] = sim
        except Exception as e:
            result_container[0] = None
            result_container[1] = str(e)
    
    # Ejecutar en thread separado con timeout
    thread = threading.Thread(target=run_backtracking)
    thread.daemon = True
    thread.start()
    thread.join(timeout=30)
    
    if thread.is_alive():
        # Timeout alcanzado
        print("      Timeout - Backtracking muy lento, usando greedy como fallback...")
        optimal_pl = greedy_playlist(small_graph, test_song.id, length=5)
        if optimal_pl:
            total_sim = sum(optimal_pl[i].similarity_score(optimal_pl[i+1]) 
                           for i in range(len(optimal_pl)-1))
            optimal_sim = total_sim
            print(f"      Playlist alternativa: {len(optimal_pl)} canciones")
    else:
        # Completado a tiempo
        optimal_pl = result_container[0]
        optimal_sim = result_container[1]
        
        if optimal_pl:
            print(f"      Generada: {len(optimal_pl)} canciones")
            print(f"      Similitud total: {optimal_sim:.3f}")
            for i, song in enumerate(optimal_pl, 1):
                print(f"      {i}. {song.title} - {song.artist}")
        elif isinstance(optimal_sim, str):
            print(f"      ERROR: {optimal_sim}")
        else:
            print("      No se encontró playlist óptima")
    
    # DIVERSA (puede usar grafo completo, es eficiente)
    print("\n    [7.3] Playlist DIVERSA (balance variedad/similitud)...")
    try:
        diverse_pl = generate_diverse_playlist(
            graph,                    # USAR GRAFO COMPLETO
            test_song.id, 
            playlist_length=8,
            diversity_weight=0.5
        )
        if diverse_pl:
            print(f"      Generada: {len(diverse_pl)} canciones")
            genres_used = set()
            for song in diverse_pl:
                genres_used.update(song.genres)
            print(f"      Géneros incluidos ({len(genres_used)}): {', '.join(list(genres_used)[:5])}")
            for i, song in enumerate(diverse_pl, 1):
                print(f"      {i}. {song.title} - {song.artist} [{', '.join(song.genres[:2])}]")
    except Exception as e:
        print(f"      ERROR: {e}")
    
    # 8. VISUALIZACIONES (LIMITADAS)
    print("\n[8] Generando visualizaciones...")
    print("    Nota: Con 2000 nodos, solo se visualizan muestras representativas")
    
    try:
        # Grafo completo - SOLO MUESTRA
        print("    [8.1] Grafo completo (muestra de 50 nodos mas conectados)...")
        VisualizationService.generate_full_graph(
            graph, 
            "outputs/test_full_graph",
            max_nodes=50,          # Limitar nodos
            min_similarity=0.5     # Solo conexiones fuertes
        )
        print("          Guardado en outputs/test_full_graph.png")
        
        # Subgrafo local
        print("    [8.2] Subgrafo local (vecindario de cancion de prueba)...")
        VisualizationService.generate_subgraph(
            graph,
            test_song.id,
            depth=2,
            output_path="outputs/test_subgraph",
            max_nodes=25
        )
        print("          Guardado en outputs/test_subgraph.png")
        
        # Red de géneros
        print("    [8.3] Red de generos (conexiones entre generos)...")
        VisualizationService.generate_genre_network(
            graph,
            "outputs/test_genre_network"
        )
        print("          Guardado en outputs/test_genre_network.png")
        
        # Visualizar playlist
        if optimal_pl and len(optimal_pl) > 1:
            print("    [8.4] Visualizacion de playlist optima...")
            similarities = [optimal_pl[i].similarity_score(optimal_pl[i+1]) 
                           for i in range(len(optimal_pl)-1)]
            VisualizationService.generate_playlist_visualization(
                optimal_pl,
                similarities,
                "outputs/test_playlist"
            )
            print("          Guardado en outputs/test_playlist.png")
        
    except Exception as e:
        print(f"    ERROR en visualizaciones: {e}")
        print("       (Asegurate de tener Graphviz instalado: 'brew install graphviz')")
    
    # 9. EXPORTAR DATOS
    print("\n[9] Exportando datos del grafo...")
    service.export_graph_data("data/graph_export.json")
    print("    Guardado en data/graph_export.json")
    
    # RESUMEN FINAL
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)
    print(f"    Canciones en dataset: {len(songs)}")
    print(f"    Nodos en grafo: {len(graph.nodes)}")
    print(f"    Conexiones totales: {graph.get_edges_count():,}")
    print(f"    Algoritmos probados: ✓ Todos")
    print(f"    Visualizaciones: outputs/")
    print(f"    Export datos: data/graph_export.json")
    print("\n    Siguiente paso: python main.py")
    print("=" * 60) 

if __name__ == "__main__":
    test_all()