import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';
import '../../core/error/exceptions.dart';
import '../../core/error/failures.dart';
import '../../domain/entities/song.dart';
import '../../domain/entities/song_recommendation.dart';
import '../../domain/entities/playlist.dart';
import '../../domain/entities/graph_stats.dart';
import '../../domain/repositories/song_repository.dart';
import '../datasources/beatnet_api_client.dart';

class SongRepositoryImpl implements SongRepository {
  final BeatNetApiClient apiClient;

  SongRepositoryImpl(this.apiClient);

  @override
  Future<Either<Failure, GraphStats>> loadData({
    double minSimilarity = 0.3,
    int? maxSongs,
  }) async {
    try {
      final response = await apiClient.loadData(minSimilarity, maxSongs);
      if (response.response.statusCode == 200) {
        final statsData = response.data['statistics'] as Map<String, dynamic>;
        final stats = _parseGraphStats(statsData);
        return Right(stats);
      }
      return const Left(ServerFailure('Failed to load data'));
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Song>>> getSongs({
    int limit = 50,
    int offset = 0,
    String sortBy = 'popularity',
  }) async {
    try {
      final response = await apiClient.getSongs(limit, offset, sortBy);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Song>> getSongById(String songId) async {
    try {
      final response = await apiClient.getSongById(songId);
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Song>> searchSongByTitle(
    String query, {
    bool fuzzy = true,
  }) async {
    try {
      final response = await apiClient.searchSongByTitle(query, fuzzy);
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Song>>> getSongsByGenre(
    String genre, {
    int limit = 50,
  }) async {
    try {
      final response = await apiClient.getSongsByGenre(genre, limit);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<SongRecommendation>>> getRecommendations(
    String songId, {
    int topK = 10,
    String method = 'graph',
  }) async {
    try {
      final response = await apiClient.getRecommendations(songId, topK, method);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Playlist>> createOptimalPlaylist(
    String songId, {
    int length = 8,
    double minSimilarity = 0.35,
  }) async {
    try {
      final response =
          await apiClient.createOptimalPlaylist(songId, length, minSimilarity);
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Playlist>> createGreedyPlaylist(
    String songId, {
    int length = 10,
  }) async {
    try {
      final response = await apiClient.createGreedyPlaylist(songId, length);
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Playlist>> createDiversePlaylist(
    String songId, {
    int length = 10,
    double diversityWeight = 0.3,
  }) async {
    try {
      final response = await apiClient.createDiversePlaylist(
          songId, length, diversityWeight);
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Song>>> searchBfs(
    String songId, {
    int maxDepth = 3,
  }) async {
    try {
      final response = await apiClient.searchBfs(songId, maxDepth);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Song>>> searchDfs(
    String songId, {
    int maxDepth = 3,
  }) async {
    try {
      final response = await apiClient.searchDfs(songId, maxDepth);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, Playlist>> findPath(
    String startId,
    String endId,
  ) async {
    try {
      final response = await apiClient.findPath(startId, endId);
      final pathData = response.data;
      return Right(pathData.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, GraphStats>> getGraphStats() async {
    try {
      final response = await apiClient.getGraphStats();
      return Right(response.data.toEntity());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<Song>>> getTopSongs(
    String criteria, {
    int k = 10,
  }) async {
    try {
      final response = await apiClient.getTopSongs(criteria, k);
      return Right(response.data.map((model) => model.toEntity()).toList());
    } on DioException catch (e) {
      return Left(_handleDioError(e));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  // Helper methods
  Failure _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const NetworkFailure('Connection timeout');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        if (statusCode == 404) {
          return const NotFoundFailure('Resource not found');
        }
        return ServerFailure(
            'Server error: ${error.response?.statusMessage ?? 'Unknown error'}');
      case DioExceptionType.cancel:
        return const NetworkFailure('Request cancelled');
      default:
        return const NetworkFailure('Network error');
    }
  }

  GraphStats _parseGraphStats(Map<String, dynamic> data) {
    return GraphStats(
      totalSongs: data['total_songs'] as int,
      totalConnections: data['total_connections'] as int,
      averageDegree: (data['average_degree'] as num).toDouble(),
      density: (data['density'] as num).toDouble(),
    );
  }
}
