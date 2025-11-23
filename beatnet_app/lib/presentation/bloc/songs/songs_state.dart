import 'package:equatable/equatable.dart';
import '../../../domain/entities/song.dart';

abstract class SongsState extends Equatable {
  const SongsState();

  @override
  List<Object?> get props => [];
}

class SongsInitial extends SongsState {
  const SongsInitial();
}

class SongsLoading extends SongsState {
  const SongsLoading();
}

class SongsLoaded extends SongsState {
  final List<Song> songs;
  final bool hasMore;
  final int currentOffset;

  const SongsLoaded({
    required this.songs,
    this.hasMore = true,
    this.currentOffset = 0,
  });

  @override
  List<Object?> get props => [songs, hasMore, currentOffset];

  SongsLoaded copyWith({
    List<Song>? songs,
    bool? hasMore,
    int? currentOffset,
  }) {
    return SongsLoaded(
      songs: songs ?? this.songs,
      hasMore: hasMore ?? this.hasMore,
      currentOffset: currentOffset ?? this.currentOffset,
    );
  }
}

class SongsLoadingMore extends SongsLoaded {
  const SongsLoadingMore({
    required super.songs,
    required super.hasMore,
    required super.currentOffset,
  });
}

class SongsError extends SongsState {
  final String message;

  const SongsError(this.message);

  @override
  List<Object?> get props => [message];
}
