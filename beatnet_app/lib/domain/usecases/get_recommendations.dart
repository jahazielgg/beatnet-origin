import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/song_recommendation.dart';
import '../repositories/song_repository.dart';

class GetRecommendations
    implements UseCase<List<SongRecommendation>, GetRecommendationsParams> {
  final SongRepository repository;

  GetRecommendations(this.repository);

  @override
  Future<Either<Failure, List<SongRecommendation>>> call(
      GetRecommendationsParams params) async {
    return await repository.getRecommendations(
      params.songId,
      topK: params.topK,
      method: params.method,
    );
  }
}

class GetRecommendationsParams {
  final String songId;
  final int topK;
  final String method;

  const GetRecommendationsParams({
    required this.songId,
    this.topK = 10,
    this.method = 'graph',
  });
}
