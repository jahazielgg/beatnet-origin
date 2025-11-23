import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../domain/entities/song.dart';
import '../../../domain/usecases/search_songs.dart';

// Events
abstract class SearchEvent extends Equatable {
  const SearchEvent();
  @override
  List<Object?> get props => [];
}

class SearchSongsEvent extends SearchEvent {
  final String query;
  final bool fuzzy;

  const SearchSongsEvent({
    required this.query,
    this.fuzzy = true,
  });

  @override
  List<Object?> get props => [query, fuzzy];
}

class ClearSearchEvent extends SearchEvent {}

// States
abstract class SearchState extends Equatable {
  const SearchState();
  @override
  List<Object?> get props => [];
}

class SearchInitial extends SearchState {}

class SearchLoading extends SearchState {}

class SearchLoaded extends SearchState {
  final Song song;

  const SearchLoaded(this.song);

  @override
  List<Object?> get props => [song];
}

class SearchError extends SearchState {
  final String message;

  const SearchError(this.message);

  @override
  List<Object?> get props => [message];
}

// BLoC
class SearchBloc extends Bloc<SearchEvent, SearchState> {
  final SearchSongs searchSongs;

  SearchBloc({required this.searchSongs}) : super(SearchInitial()) {
    on<SearchSongsEvent>(_onSearchSongs);
    on<ClearSearchEvent>(_onClearSearch);
  }

  Future<void> _onSearchSongs(
    SearchSongsEvent event,
    Emitter<SearchState> emit,
  ) async {
    if (event.query.isEmpty) {
      emit(SearchInitial());
      return;
    }

    emit(SearchLoading());

    final result = await searchSongs(SearchSongsParams(
      query: event.query,
      fuzzy: event.fuzzy,
    ));

    result.fold(
      (failure) => emit(SearchError(failure.message)),
      (song) => emit(SearchLoaded(song)),
    );
  }

  void _onClearSearch(
    ClearSearchEvent event,
    Emitter<SearchState> emit,
  ) {
    emit(SearchInitial());
  }
}
