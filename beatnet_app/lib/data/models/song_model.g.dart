// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'song_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

SongModel _$SongModelFromJson(Map<String, dynamic> json) => SongModel(
      id: json['id'] as String,
      title: json['title'] as String,
      artist: json['artist'] as String,
      genres:
          (json['genres'] as List<dynamic>).map((e) => e as String).toList(),
      duration: (json['duration'] as num).toInt(),
      year: (json['year'] as num?)?.toInt(),
      popularity: (json['popularity'] as num).toInt(),
      previewUrl: json['preview_url'] as String,
      coverUrl: json['cover_url'] as String,
      deezerId: json['deezer_id'] as String?,
    );

Map<String, dynamic> _$SongModelToJson(SongModel instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'artist': instance.artist,
      'genres': instance.genres,
      'duration': instance.duration,
      'year': instance.year,
      'popularity': instance.popularity,
      'preview_url': instance.previewUrl,
      'cover_url': instance.coverUrl,
      'deezer_id': instance.deezerId,
    };
