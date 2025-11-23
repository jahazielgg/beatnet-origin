import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/song.dart';
import '../repositories/song_repository.dart';

class GetSongs implements UseCase<List<Song>, GetSongsParams> {
  final SongRepository repository;

  GetSongs(this.repository);

  @override
  Future<Either<Failure, List<Song>>> call(GetSongsParams params) async {
    return await repository.getSongs(
      limit: params.limit,
      offset: params.offset,
      sortBy: params.sortBy,
    );
  }
}

class GetSongsParams {
  final int limit;
  final int offset;
  final String sortBy;

  const GetSongsParams({
    this.limit = 50,
    this.offset = 0,
    this.sortBy = 'popularity',
  });
}
