import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/usecases/get_songs.dart';
import 'songs_event.dart';
import 'songs_state.dart';

class SongsBloc extends Bloc<SongsEvent, SongsState> {
  final GetSongs getSongs;

  SongsBloc({required this.getSongs}) : super(const SongsInitial()) {
    on<LoadSongsEvent>(_onLoadSongs);
    on<RefreshSongsEvent>(_onRefreshSongs);
  }

  Future<void> _onLoadSongs(
    LoadSongsEvent event,
    Emitter<SongsState> emit,
  ) async {
    if (event.loadMore && state is SongsLoaded) {
      final currentState = state as SongsLoaded;
      emit(SongsLoadingMore(
        songs: currentState.songs,
        hasMore: currentState.hasMore,
        currentOffset: currentState.currentOffset,
      ));
    } else {
      emit(const SongsLoading());
    }

    final result = await getSongs(GetSongsParams(
      limit: event.limit,
      offset: event.offset,
      sortBy: event.sortBy,
    ));

    result.fold(
      (failure) => emit(SongsError(failure.message)),
      (songs) {
        if (event.loadMore && state is SongsLoadingMore) {
          final currentState = state as SongsLoadingMore;
          emit(SongsLoaded(
            songs: [...currentState.songs, ...songs],
            hasMore: songs.length >= event.limit,
            currentOffset: event.offset,
          ));
        } else {
          emit(SongsLoaded(
            songs: songs,
            hasMore: songs.length >= event.limit,
            currentOffset: event.offset,
          ));
        }
      },
    );
  }

  Future<void> _onRefreshSongs(
    RefreshSongsEvent event,
    Emitter<SongsState> emit,
  ) async {
    emit(const SongsLoading());
    add(const LoadSongsEvent());
  }
}
