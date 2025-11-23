import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/song.dart';

part 'song_model.g.dart';

@JsonSerializable()
class SongModel extends Song {
  const SongModel({
    required super.id,
    required super.title,
    required super.artist,
    required super.genres,
    required super.duration,
    super.year,
    required super.popularity,
    required super.previewUrl,
    required super.coverUrl,
    super.deezerId,
  });

  factory SongModel.fromJson(Map<String, dynamic> json) {
    return SongModel(
      id: json['id'].toString(),
      title: json['title'] as String,
      artist: json['artist'] as String,
      genres: (json['genres'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
      duration: json['duration'] as int? ?? 0,
      year: json['year'] as int?,
      popularity: json['popularity'] as int? ?? 0,
      previewUrl: json['preview_url'] as String? ?? '',
      coverUrl: json['cover_url'] as String? ?? '',
      deezerId: json['deezer_id']?.toString(),
    );
  }

  Map<String, dynamic> toJson() => _$SongModelToJson(this);

  factory SongModel.fromEntity(Song song) {
    return SongModel(
      id: song.id,
      title: song.title,
      artist: song.artist,
      genres: song.genres,
      duration: song.duration,
      year: song.year,
      popularity: song.popularity,
      previewUrl: song.previewUrl,
      coverUrl: song.coverUrl,
      deezerId: song.deezerId,
    );
  }

  Song toEntity() => this;
}
