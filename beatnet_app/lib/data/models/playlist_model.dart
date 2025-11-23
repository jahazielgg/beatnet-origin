import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/playlist.dart';
import 'song_model.dart';

part 'playlist_model.g.dart';

@JsonSerializable()
class PlaylistModel extends Playlist {
  const PlaylistModel({
    required super.songs,
    required super.totalSimilarity,
    required super.algorithmUsed,
  });

  factory PlaylistModel.fromJson(Map<String, dynamic> json) {
    return PlaylistModel(
      songs: (json['songs'] as List<dynamic>)
          .map((e) => SongModel.fromJson(e as Map<String, dynamic>))
          .toList(),
      totalSimilarity: (json['total_similarity'] as num).toDouble(),
      algorithmUsed: json['algorithm_used'] as String,
    );
  }

  Map<String, dynamic> toJson() => _$PlaylistModelToJson(this);

  Playlist toEntity() => this;
}
