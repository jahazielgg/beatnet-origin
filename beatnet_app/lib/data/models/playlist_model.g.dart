// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'playlist_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

PlaylistModel _$PlaylistModelFromJson(Map<String, dynamic> json) =>
    PlaylistModel(
      songs: (json['songs'] as List<dynamic>)
          .map((e) => SongModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalSimilarity: (json['total_similarity'] as num).toDouble(),
      algorithmUsed: json['algorithm_used'] as String,
    );

Map<String, dynamic> _$PlaylistModelToJson(PlaylistModel instance) =>
    <String, dynamic>{
      'songs': instance.songs,
      'total_similarity': instance.totalSimilarity,
      'algorithm_used': instance.algorithmUsed,
    };
