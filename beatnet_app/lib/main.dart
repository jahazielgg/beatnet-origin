import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'config/theme/app_theme.dart';
import 'core/di/injection_container.dart' as di;
import 'presentation/bloc/songs/songs_bloc.dart';
import 'presentation/bloc/recommendations/recommendations_bloc.dart';
import 'presentation/bloc/playlist/playlist_bloc.dart';
import 'presentation/bloc/search/search_bloc.dart';
import 'presentation/pages/home/home_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => di.sl<SongsBloc>()),
        BlocProvider(create: (_) => di.sl<RecommendationsBloc>()),
        BlocProvider(create: (_) => di.sl<PlaylistBloc>()),
        BlocProvider(create: (_) => di.sl<SearchBloc>()),
      ],
      child: MaterialApp(
        title: 'BeatNet',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.darkTheme,
        home: const HomePage(),
      ),
    );
  }
}
