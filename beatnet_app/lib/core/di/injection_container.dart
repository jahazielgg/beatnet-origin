import 'package:get_it/get_it.dart';
import '../../data/datasources/beatnet_api_client.dart';
import '../../data/repositories/song_repository_impl.dart';
import '../../domain/repositories/song_repository.dart';
import '../../domain/usecases/get_songs.dart';
import '../../domain/usecases/get_recommendations.dart';
import '../../domain/usecases/create_playlist.dart';
import '../../domain/usecases/search_songs.dart';
import '../../presentation/bloc/songs/songs_bloc.dart';
import '../../presentation/bloc/recommendations/recommendations_bloc.dart';
import '../../presentation/bloc/playlist/playlist_bloc.dart';
import '../../presentation/bloc/search/search_bloc.dart';
import '../network/dio_client.dart';

final sl = GetIt.instance;

Future<void> init() async {
  // BLoCs
  sl.registerFactory(() => SongsBloc(getSongs: sl()));
  sl.registerFactory(() => RecommendationsBloc(getRecommendations: sl()));
  sl.registerFactory(() => PlaylistBloc(createPlaylist: sl()));
  sl.registerFactory(() => SearchBloc(searchSongs: sl()));

  // Use cases
  sl.registerLazySingleton(() => GetSongs(sl()));
  sl.registerLazySingleton(() => GetRecommendations(sl()));
  sl.registerLazySingleton(() => CreatePlaylist(sl()));
  sl.registerLazySingleton(() => SearchSongs(sl()));

  // Repository
  sl.registerLazySingleton<SongRepository>(
    () => SongRepositoryImpl(sl()),
  );

  // Data sources
  sl.registerLazySingleton<BeatNetApiClient>(
    () => BeatNetApiClient(sl()),
  );

  // External
  sl.registerLazySingleton(() => DioClient.createDio());
}
