import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../domain/entities/playlist.dart';
import '../../../domain/usecases/create_playlist.dart';

// Events
abstract class PlaylistEvent extends Equatable {
  const PlaylistEvent();
  @override
  List<Object?> get props => [];
}

class CreatePlaylistEvent extends PlaylistEvent {
  final String songId;
  final int length;
  final PlaylistType type;
  final double? minSimilarity;
  final double? diversityWeight;

  const CreatePlaylistEvent({
    required this.songId,
    this.length = 8,
    this.type = PlaylistType.greedy,
    this.minSimilarity,
    this.diversityWeight,
  });

  @override
  List<Object?> get props =>
      [songId, length, type, minSimilarity, diversityWeight];
}

// States
abstract class PlaylistState extends Equatable {
  const PlaylistState();
  @override
  List<Object?> get props => [];
}

class PlaylistInitial extends PlaylistState {}

class PlaylistLoading extends PlaylistState {}

class PlaylistLoaded extends PlaylistState {
  final Playlist playlist;

  const PlaylistLoaded(this.playlist);

  @override
  List<Object?> get props => [playlist];
}

class PlaylistError extends PlaylistState {
  final String message;

  const PlaylistError(this.message);

  @override
  List<Object?> get props => [message];
}

// BLoC
class PlaylistBloc extends Bloc<PlaylistEvent, PlaylistState> {
  final CreatePlaylist createPlaylist;

  PlaylistBloc({required this.createPlaylist}) : super(PlaylistInitial()) {
    on<CreatePlaylistEvent>(_onCreatePlaylist);
  }

  Future<void> _onCreatePlaylist(
    CreatePlaylistEvent event,
    Emitter<PlaylistState> emit,
  ) async {
    emit(PlaylistLoading());

    final result = await createPlaylist(CreatePlaylistParams(
      songId: event.songId,
      length: event.length,
      type: event.type,
      minSimilarity: event.minSimilarity,
      diversityWeight: event.diversityWeight,
    ));

    result.fold(
      (failure) => emit(PlaylistError(failure.message)),
      (playlist) => emit(PlaylistLoaded(playlist)),
    );
  }
}
