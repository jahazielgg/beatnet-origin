import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/graph_stats.dart';

part 'graph_stats_model.g.dart';

@JsonSerializable()
class GraphStatsModel extends GraphStats {
  const GraphStatsModel({
    required super.totalSongs,
    required super.totalConnections,
    required super.averageDegree,
    required super.density,
  });

  factory GraphStatsModel.fromJson(Map<String, dynamic> json) {
    return GraphStatsModel(
      totalSongs: json['total_songs'] as int,
      totalConnections: json['total_connections'] as int,
      averageDegree: (json['average_degree'] as num).toDouble(),
      density: (json['density'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => _$GraphStatsModelToJson(this);

  GraphStats toEntity() => this;
}
