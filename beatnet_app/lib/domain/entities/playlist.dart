import 'package:equatable/equatable.dart';
import 'song.dart';

class Playlist extends Equatable {
  final List<Song> songs;
  final double totalSimilarity;
  final String algorithmUsed;

  const Playlist({
    required this.songs,
    required this.totalSimilarity,
    required this.algorithmUsed,
  });

  int get totalDuration => songs.fold(0, (sum, song) => sum + song.duration);

  String get totalDurationFormatted {
    final minutes = totalDuration ~/ 60;
    final seconds = totalDuration % 60;
    return '$minutes:${seconds.toString().padLeft(2, '0')}';
  }

  String get algorithmDisplayName {
    switch (algorithmUsed.toLowerCase()) {
      case 'backtracking':
        return 'Optimal (Backtracking)';
      case 'greedy':
        return 'Greedy Algorithm';
      case 'diverse_backtracking':
        return 'Diverse Mix';
      default:
        return algorithmUsed;
    }
  }

  @override
  List<Object?> get props => [songs, totalSimilarity, algorithmUsed];
}
