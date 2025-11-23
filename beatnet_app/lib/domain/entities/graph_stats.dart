import 'package:equatable/equatable.dart';

class GraphStats extends Equatable {
  final int totalSongs;
  final int totalConnections;
  final double averageDegree;
  final double density;

  const GraphStats({
    required this.totalSongs,
    required this.totalConnections,
    required this.averageDegree,
    required this.density,
  });

  String get densityPercentage => '${(density * 100).toStringAsFixed(2)}%';

  @override
  List<Object?> get props => [
        totalSongs,
        totalConnections,
        averageDegree,
        density,
      ];
}
