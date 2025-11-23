import 'package:equatable/equatable.dart';
import 'song.dart';

class SongRecommendation extends Equatable {
  final Song song;
  final double similarity;

  const SongRecommendation({
    required this.song,
    required this.similarity,
  });

  String get similarityPercentage => '${(similarity * 100).toStringAsFixed(0)}%';

  @override
  List<Object?> get props => [song, similarity];
}
