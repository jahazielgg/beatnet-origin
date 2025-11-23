import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';
import '../../core/constants/api_constants.dart';
import '../models/song_model.dart';
import '../models/playlist_model.dart';
import '../models/song_recommendation_model.dart';
import '../models/graph_stats_model.dart';

part 'beatnet_api_client.g.dart';

@RestApi(baseUrl: ApiConstants.baseUrl)
abstract class BeatNetApiClient {
  factory BeatNetApiClient(Dio dio, {String baseUrl}) = _BeatNetApiClient;

  @POST('${ApiConstants.apiPrefix}${ApiConstants.load}')
  Future<HttpResponse<Map<String, dynamic>>> loadData(
    @Query(ApiConstants.minSimilarity) double minSimilarity,
    @Query(ApiConstants.maxSongs) int? maxSongs,
  );

  @GET('${ApiConstants.apiPrefix}${ApiConstants.songs}')
  Future<HttpResponse<List<SongModel>>> getSongs(
    @Query(ApiConstants.limit) int limit,
    @Query(ApiConstants.offset) int offset,
    @Query(ApiConstants.sortBy) String sortBy,
  );

  @GET('${ApiConstants.apiPrefix}/songs/{id}')
  Future<HttpResponse<SongModel>> getSongById(
    @Path('id') String songId,
  );

  @GET('${ApiConstants.apiPrefix}${ApiConstants.searchSongs}')
  Future<HttpResponse<SongModel>> searchSongByTitle(
    @Query(ApiConstants.query) String query,
    @Query(ApiConstants.fuzzy) bool fuzzy,
  );

  @GET('${ApiConstants.apiPrefix}/songs/genre/{genre}')
  Future<HttpResponse<List<SongModel>>> getSongsByGenre(
    @Path('genre') String genre,
    @Query(ApiConstants.limit) int limit,
  );

  @GET('${ApiConstants.apiPrefix}/recommendations/{song_id}')
  Future<HttpResponse<List<SongRecommendationModel>>> getRecommendations(
    @Path('song_id') String songId,
    @Query(ApiConstants.topK) int topK,
    @Query(ApiConstants.method) String method,
  );

  @POST('${ApiConstants.apiPrefix}${ApiConstants.playlistOptimal}')
  Future<HttpResponse<PlaylistModel>> createOptimalPlaylist(
    @Query(ApiConstants.songId) String songId,
    @Query(ApiConstants.length) int length,
    @Query(ApiConstants.minSimilarity) double minSimilarity,
  );

  @POST('${ApiConstants.apiPrefix}${ApiConstants.playlistGreedy}')
  Future<HttpResponse<PlaylistModel>> createGreedyPlaylist(
    @Query(ApiConstants.songId) String songId,
    @Query(ApiConstants.length) int length,
  );

  @POST('${ApiConstants.apiPrefix}${ApiConstants.playlistDiverse}')
  Future<HttpResponse<PlaylistModel>> createDiversePlaylist(
    @Query(ApiConstants.songId) String songId,
    @Query(ApiConstants.length) int length,
    @Query(ApiConstants.diversityWeight) double diversityWeight,
  );

  @GET('${ApiConstants.apiPrefix}/search/bfs/{song_id}')
  Future<HttpResponse<List<SongModel>>> searchBfs(
    @Path('song_id') String songId,
    @Query(ApiConstants.maxDepth) int maxDepth,
  );

  @GET('${ApiConstants.apiPrefix}/search/dfs/{song_id}')
  Future<HttpResponse<List<SongModel>>> searchDfs(
    @Path('song_id') String songId,
    @Query(ApiConstants.maxDepth) int maxDepth,
  );

  @GET('${ApiConstants.apiPrefix}/path/{start_id}/{end_id}')
  Future<HttpResponse<PlaylistModel>> findPath(
    @Path('start_id') String startId,
    @Path('end_id') String endId,
  );

  @GET('${ApiConstants.apiPrefix}${ApiConstants.stats}')
  Future<HttpResponse<GraphStatsModel>> getGraphStats();

  @GET('${ApiConstants.apiPrefix}/top/{criteria}')
  Future<HttpResponse<List<SongModel>>> getTopSongs(
    @Path('criteria') String criteria,
    @Query(ApiConstants.k) int k,
  );
}
