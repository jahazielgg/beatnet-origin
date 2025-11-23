import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../entities/song.dart';
import '../entities/song_recommendation.dart';
import '../entities/playlist.dart';
import '../entities/graph_stats.dart';

abstract class SongRepository {
  /// Carga los datos y construye el grafo
  Future<Either<Failure, GraphStats>> loadData({
    double minSimilarity = 0.3,
    int? maxSongs,
  });

  /// Obtiene lista de canciones con paginación
  Future<Either<Failure, List<Song>>> getSongs({
    int limit = 50,
    int offset = 0,
    String sortBy = 'popularity',
  });

  /// Obtiene una canción por ID
  Future<Either<Failure, Song>> getSongById(String songId);

  /// Busca canciones por título
  Future<Either<Failure, Song>> searchSongByTitle(
    String query, {
    bool fuzzy = true,
  });

  /// Obtiene canciones por género
  Future<Either<Failure, List<Song>>> getSongsByGenre(
    String genre, {
    int limit = 50,
  });

  /// Obtiene recomendaciones para una canción
  Future<Either<Failure, List<SongRecommendation>>> getRecommendations(
    String songId, {
    int topK = 10,
    String method = 'graph',
  });

  /// Crea playlist óptima usando backtracking
  Future<Either<Failure, Playlist>> createOptimalPlaylist(
    String songId, {
    int length = 8,
    double minSimilarity = 0.35,
  });

  /// Crea playlist usando algoritmo greedy
  Future<Either<Failure, Playlist>> createGreedyPlaylist(
    String songId, {
    int length = 10,
  });

  /// Crea playlist diversa
  Future<Either<Failure, Playlist>> createDiversePlaylist(
    String songId, {
    int length = 10,
    double diversityWeight = 0.3,
  });

  /// Búsqueda BFS desde una canción
  Future<Either<Failure, List<Song>>> searchBfs(
    String songId, {
    int maxDepth = 3,
  });

  /// Búsqueda DFS desde una canción
  Future<Either<Failure, List<Song>>> searchDfs(
    String songId, {
    int maxDepth = 3,
  });

  /// Encuentra camino entre dos canciones (Dijkstra)
  Future<Either<Failure, Playlist>> findPath(
    String startId,
    String endId,
  );

  /// Obtiene estadísticas del grafo
  Future<Either<Failure, GraphStats>> getGraphStats();

  /// Obtiene top K canciones por criterio
  Future<Either<Failure, List<Song>>> getTopSongs(
    String criteria, {
    int k = 10,
  });
}
