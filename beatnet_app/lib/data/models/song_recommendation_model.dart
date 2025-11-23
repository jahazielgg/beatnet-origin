import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/song_recommendation.dart';
import 'song_model.dart';

part 'song_recommendation_model.g.dart';

@JsonSerializable()
class SongRecommendationModel extends SongRecommendation {
  const SongRecommendationModel({
    required super.song,
    required super.similarity,
  });

  factory SongRecommendationModel.fromJson(Map<String, dynamic> json) {
    return SongRecommendationModel(
      song: SongModel.fromJson(json['song'] as Map<String, dynamic>),
      similarity: (json['similarity'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => _$SongRecommendationModelToJson(this);

  SongRecommendation toEntity() => this;
}
