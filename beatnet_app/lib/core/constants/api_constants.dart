class ApiConstants {
  // Base URL - CAMBIAR según tu configuración
  static const String baseUrl = 'http://localhost:8000';
  static const String apiPrefix = '/api/v1';

  // Timeouts
  static const int connectionTimeout = 30000; // 30 segundos
  static const int receiveTimeout = 30000;

  // Endpoints
  static const String load = '/load';
  static const String songs = '/songs';
  static const String songById = '/songs/{id}';
  static const String searchSongs = '/songs/search/title';
  static const String songsByGenre = '/songs/genre/{genre}';
  static const String recommendations = '/recommendations/{song_id}';
  static const String playlistOptimal = '/playlist/optimal';
  static const String playlistGreedy = '/playlist/greedy';
  static const String playlistDiverse = '/playlist/diverse';
  static const String searchBfs = '/search/bfs/{song_id}';
  static const String searchDfs = '/search/dfs/{song_id}';
  static const String path = '/path/{start_id}/{end_id}';
  static const String stats = '/stats';
  static const String statsGenres = '/stats/genres';
  static const String statsArtists = '/stats/artists';
  static const String topSongs = '/top/{criteria}';

  // Query Parameters
  static const String minSimilarity = 'min_similarity';
  static const String maxSongs = 'max_songs';
  static const String limit = 'limit';
  static const String offset = 'offset';
  static const String sortBy = 'sort_by';
  static const String query = 'q';
  static const String fuzzy = 'fuzzy';
  static const String topK = 'top_k';
  static const String method = 'method';
  static const String songId = 'song_id';
  static const String length = 'length';
  static const String diversityWeight = 'diversity_weight';
  static const String maxDepth = 'max_depth';
  static const String k = 'k';

  ApiConstants._();
}
