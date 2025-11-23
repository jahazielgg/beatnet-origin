import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../../domain/entities/song_recommendation.dart';
import '../../../domain/usecases/get_recommendations.dart';

// Events
abstract class RecommendationsEvent extends Equatable {
  const RecommendationsEvent();
  @override
  List<Object?> get props => [];
}

class LoadRecommendationsEvent extends RecommendationsEvent {
  final String songId;
  final int topK;
  final String method;

  const LoadRecommendationsEvent({
    required this.songId,
    this.topK = 10,
    this.method = 'graph',
  });

  @override
  List<Object?> get props => [songId, topK, method];
}

// States
abstract class RecommendationsState extends Equatable {
  const RecommendationsState();
  @override
  List<Object?> get props => [];
}

class RecommendationsInitial extends RecommendationsState {}

class RecommendationsLoading extends RecommendationsState {}

class RecommendationsLoaded extends RecommendationsState {
  final List<SongRecommendation> recommendations;

  const RecommendationsLoaded(this.recommendations);

  @override
  List<Object?> get props => [recommendations];
}

class RecommendationsError extends RecommendationsState {
  final String message;

  const RecommendationsError(this.message);

  @override
  List<Object?> get props => [message];
}

// BLoC
class RecommendationsBloc
    extends Bloc<RecommendationsEvent, RecommendationsState> {
  final GetRecommendations getRecommendations;

  RecommendationsBloc({required this.getRecommendations})
      : super(RecommendationsInitial()) {
    on<LoadRecommendationsEvent>(_onLoadRecommendations);
  }

  Future<void> _onLoadRecommendations(
    LoadRecommendationsEvent event,
    Emitter<RecommendationsState> emit,
  ) async {
    emit(RecommendationsLoading());

    final result = await getRecommendations(GetRecommendationsParams(
      songId: event.songId,
      topK: event.topK,
      method: event.method,
    ));

    result.fold(
      (failure) => emit(RecommendationsError(failure.message)),
      (recommendations) => emit(RecommendationsLoaded(recommendations)),
    );
  }
}
