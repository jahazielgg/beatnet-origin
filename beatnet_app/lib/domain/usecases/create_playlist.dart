import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/playlist.dart';
import '../repositories/song_repository.dart';

enum PlaylistType { optimal, greedy, diverse }

class CreatePlaylist implements UseCase<Playlist, CreatePlaylistParams> {
  final SongRepository repository;

  CreatePlaylist(this.repository);

  @override
  Future<Either<Failure, Playlist>> call(CreatePlaylistParams params) async {
    switch (params.type) {
      case PlaylistType.optimal:
        return await repository.createOptimalPlaylist(
          params.songId,
          length: params.length,
          minSimilarity: params.minSimilarity ?? 0.35,
        );
      case PlaylistType.greedy:
        return await repository.createGreedyPlaylist(
          params.songId,
          length: params.length,
        );
      case PlaylistType.diverse:
        return await repository.createDiversePlaylist(
          params.songId,
          length: params.length,
          diversityWeight: params.diversityWeight ?? 0.3,
        );
    }
  }
}

class CreatePlaylistParams {
  final String songId;
  final int length;
  final PlaylistType type;
  final double? minSimilarity;
  final double? diversityWeight;

  const CreatePlaylistParams({
    required this.songId,
    this.length = 8,
    this.type = PlaylistType.greedy,
    this.minSimilarity,
    this.diversityWeight,
  });
}
