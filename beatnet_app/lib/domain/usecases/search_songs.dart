import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/song.dart';
import '../repositories/song_repository.dart';

class SearchSongs implements UseCase<Song, SearchSongsParams> {
  final SongRepository repository;

  SearchSongs(this.repository);

  @override
  Future<Either<Failure, Song>> call(SearchSongsParams params) async {
    return await repository.searchSongByTitle(
      params.query,
      fuzzy: params.fuzzy,
    );
  }
}

class SearchSongsParams {
  final String query;
  final bool fuzzy;

  const SearchSongsParams({
    required this.query,
    this.fuzzy = true,
  });
}
