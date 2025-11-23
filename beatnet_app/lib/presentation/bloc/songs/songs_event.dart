import 'package:equatable/equatable.dart';

abstract class SongsEvent extends Equatable {
  const SongsEvent();

  @override
  List<Object?> get props => [];
}

class LoadSongsEvent extends SongsEvent {
  final int limit;
  final int offset;
  final String sortBy;
  final bool loadMore;

  const LoadSongsEvent({
    this.limit = 50,
    this.offset = 0,
    this.sortBy = 'popularity',
    this.loadMore = false,
  });

  @override
  List<Object?> get props => [limit, offset, sortBy, loadMore];
}

class RefreshSongsEvent extends SongsEvent {
  const RefreshSongsEvent();
}
