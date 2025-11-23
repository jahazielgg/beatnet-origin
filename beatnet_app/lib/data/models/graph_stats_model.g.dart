// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'graph_stats_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

GraphStatsModel _$GraphStatsModelFromJson(Map<String, dynamic> json) =>
    GraphStatsModel(
      totalSongs: (json['total_songs'] as num).toInt(),
      totalConnections: (json['total_connections'] as num).toInt(),
      averageDegree: (json['average_degree'] as num).toDouble(),
      density: (json['density'] as num).toDouble(),
    );

Map<String, dynamic> _$GraphStatsModelToJson(GraphStatsModel instance) =>
    <String, dynamic>{
      'total_songs': instance.totalSongs,
      'total_connections': instance.totalConnections,
      'average_degree': instance.averageDegree,
      'density': instance.density,
    };
