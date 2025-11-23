// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'song_recommendation_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SongRecommendationModel _$SongRecommendationModelFromJson(
        Map<String, dynamic> json) =>
    SongRecommendationModel(
      song: SongModel.fromJson(json['song'] as Map<String, dynamic>),
      similarity: (json['similarity'] as num).toDouble(),
    );

Map<String, dynamic> _$SongRecommendationModelToJson(
        SongRecommendationModel instance) =>
    <String, dynamic>{
      'song': instance.song,
      'similarity': instance.similarity,
    };
