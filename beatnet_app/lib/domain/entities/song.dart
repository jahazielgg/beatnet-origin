import 'package:equatable/equatable.dart';

class Song extends Equatable {
  final String id;
  final String title;
  final String artist;
  final List<String> genres;
  final int duration;
  final int? year;
  final int popularity;
  final String previewUrl;
  final String coverUrl;
  final String? deezerId;

  const Song({
    required this.id,
    required this.title,
    required this.artist,
    required this.genres,
    required this.duration,
    this.year,
    required this.popularity,
    required this.previewUrl,
    required this.coverUrl,
    this.deezerId,
  });

  String get durationFormatted {
    final minutes = duration ~/ 60;
    final seconds = duration % 60;
    return '$minutes:${seconds.toString().padLeft(2, '0')}';
  }

  String get yearDisplay => year?.toString() ?? 'Unknown';

  String get genresDisplay => genres.join(', ');

  @override
  List<Object?> get props => [
        id,
        title,
        artist,
        genres,
        duration,
        year,
        popularity,
        previewUrl,
        coverUrl,
        deezerId,
      ];
}
