import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../config/theme/app_theme.dart';
import '../../bloc/songs/songs_bloc.dart';
import '../../bloc/songs/songs_event.dart';
import '../../bloc/songs/songs_state.dart';
import '../../widgets/song_card.dart';
import '../../widgets/loading_shimmer.dart';
import '../song_details/song_details_page.dart';
import '../search/search_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final ScrollController _scrollController = ScrollController();
  String _currentSort = 'popularity';

  @override
  void initState() {
    super.initState();
    context.read<SongsBloc>().add(const LoadSongsEvent());
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_isBottom) {
      final state = context.read<SongsBloc>().state;
      if (state is SongsLoaded && state.hasMore) {
        context.read<SongsBloc>().add(LoadSongsEvent(
              offset: state.currentOffset + 50,
              sortBy: _currentSort,
              loadMore: true,
            ));
      }
    }
  }

  bool get _isBottom {
    if (!_scrollController.hasClients) return false;
    final maxScroll = _scrollController.position.maxScrollExtent;
    final currentScroll = _scrollController.offset;
    return currentScroll >= (maxScroll * 0.9);
  }

  void _changeSortOrder(String sortBy) {
    setState(() {
      _currentSort = sortBy;
    });
    context.read<SongsBloc>().add(LoadSongsEvent(sortBy: sortBy));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        controller: _scrollController,
        slivers: [
          _buildAppBar(),
          _buildSortOptions(),
          _buildSongsList(),
        ],
      ),
    );
  }

  Widget _buildAppBar() {
    return SliverAppBar(
      expandedHeight: 240,
      floating: false,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        centerTitle: true,
        title: const Text(
          'BeatNet',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: 1,
          ),
        ),
        background: Container(
          decoration: const BoxDecoration(
            gradient: AppTheme.primaryGradient,
          ),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.only(bottom: 20.0),
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.15),
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.2),
                              blurRadius: 20,
                              spreadRadius: 2,
                            ),
                          ],
                        ),
                        child: const Icon(
                          Icons.music_note_rounded,
                          size: 80,
                          color: Colors.white,
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
      actions: [
        IconButton(
          icon: const Icon(Icons.search),
          tooltip: 'Buscar',
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const SearchPage(),
              ),
            );
          },
        ),
        const SizedBox(width: 8),
      ],
    );
  }

  Widget _buildSortOptions() {
    return SliverToBoxAdapter(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        margin: const EdgeInsets.only(top: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Ordenar por:',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
            ),
            const SizedBox(height: 12),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildSortChip('Popularidad', 'popularity'),
                  const SizedBox(width: 8),
                  _buildSortChip('Título', 'title'),
                  const SizedBox(width: 8),
                  _buildSortChip('Año', 'year'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSortChip(String label, String value) {
    final isSelected = _currentSort == value;
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (_) => _changeSortOrder(value),
      backgroundColor: AppTheme.surfaceColor,
      selectedColor: AppTheme.primaryColor,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      labelStyle: TextStyle(
        color: isSelected ? Colors.white : AppTheme.textSecondaryColor,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
        fontSize: 14,
      ),
      elevation: isSelected ? 4 : 0,
      shadowColor: AppTheme.primaryColor.withOpacity(0.5),
    );
  }

  Widget _buildSongsList() {
    return BlocBuilder<SongsBloc, SongsState>(
      builder: (context, state) {
        if (state is SongsLoading) {
          return const SliverToBoxAdapter(
            child: LoadingShimmer(),
          );
        }

        if (state is SongsError) {
          return SliverFillRemaining(
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    size: 64,
                    color: AppTheme.errorColor,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Error al cargar canciones',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    state.message,
                    style: Theme.of(context).textTheme.bodyMedium,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: () {
                      context
                          .read<SongsBloc>()
                          .add(LoadSongsEvent(sortBy: _currentSort));
                    },
                    icon: const Icon(Icons.refresh),
                    label: const Text('Reintentar'),
                  ),
                ],
              ),
            ),
          );
        }

        if (state is SongsLoaded || state is SongsLoadingMore) {
          final songs = state is SongsLoaded
              ? state.songs
              : (state as SongsLoadingMore).songs;

          if (songs.isEmpty) {
            return const SliverFillRemaining(
              child: Center(
                child: Text('No hay canciones disponibles'),
              ),
            );
          }

          return SliverPadding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            sliver: SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  if (index >= songs.length) {
                    return const Center(
                      child: Padding(
                        padding: EdgeInsets.symmetric(vertical: 24.0),
                        child: CircularProgressIndicator(),
                      ),
                    );
                  }

                  final song = songs[index];
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: SongCard(
                      song: song,
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => SongDetailsPage(song: song),
                          ),
                        );
                      },
                    ),
                  );
                },
                childCount: songs.length + (state is SongsLoadingMore ? 1 : 0),
              ),
            ),
          );
        }

        return const SliverFillRemaining(
          child: Center(
            child: Text('Presiona el botón para cargar canciones'),
          ),
        );
      },
    );
  }
}
