import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../../domain/entities/song.dart';
import '../../../domain/usecases/create_playlist.dart';
import '../../../config/theme/app_theme.dart';
import '../../bloc/recommendations/recommendations_bloc.dart';
import '../../bloc/playlist/playlist_bloc.dart';
import '../../widgets/song_card.dart';
import '../playlist/playlist_page.dart';

class SongDetailsPage extends StatefulWidget {
  final Song song;

  const SongDetailsPage({super.key, required this.song});

  @override
  State<SongDetailsPage> createState() => _SongDetailsPageState();
}

class _SongDetailsPageState extends State<SongDetailsPage> {
  @override
  void initState() {
    super.initState();
    context.read<RecommendationsBloc>().add(
          LoadRecommendationsEvent(songId: widget.song.id),
        );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          _buildAppBar(),
          _buildSongInfo(),
          _buildActionsSection(),
          _buildRecommendationsSection(),
        ],
      ),
    );
  }

  Widget _buildAppBar() {
    return SliverAppBar(
      expandedHeight: 300,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        background: Stack(
          fit: StackFit.expand,
          children: [
            CachedNetworkImage(
              imageUrl: widget.song.coverUrl,
              fit: BoxFit.cover,
            ),
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.transparent,
                    AppTheme.backgroundColor.withOpacity(0.8),
                    AppTheme.backgroundColor,
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSongInfo() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.song.title,
              style: Theme.of(context).textTheme.displaySmall,
            ),
            const SizedBox(height: 8),
            Text(
              widget.song.artist,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    color: AppTheme.textSecondaryColor,
                  ),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: widget.song.genres.map((genre) {
                return Chip(
                  label: Text(genre),
                  backgroundColor: AppTheme.primaryColor.withOpacity(0.2),
                  labelStyle: const TextStyle(
                    color: AppTheme.primaryColor,
                    fontWeight: FontWeight.w600,
                  ),
                );
              }).toList(),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                _buildInfoChip(
                  Icons.timer,
                  widget.song.durationFormatted,
                ),
                const SizedBox(width: 12),
                _buildInfoChip(
                  Icons.calendar_today,
                  widget.song.yearDisplay,
                ),
                const SizedBox(width: 12),
                _buildInfoChip(
                  Icons.trending_up,
                  '${widget.song.popularity}',
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoChip(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: AppTheme.textSecondaryColor),
          const SizedBox(width: 4),
          Text(
            label,
            style: Theme.of(context).textTheme.bodySmall,
          ),
        ],
      ),
    );
  }

  Widget _buildActionsSection() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Divider(height: 32),
            Text(
              'Crear Playlist',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildPlaylistButton(
                    'Óptima',
                    'Backtracking',
                    Icons.auto_awesome,
                    AppTheme.primaryColor,
                    PlaylistType.optimal,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildPlaylistButton(
                    'Rápida',
                    'Greedy',
                    Icons.flash_on,
                    AppTheme.accentColor,
                    PlaylistType.greedy,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            _buildPlaylistButton(
              'Diversa',
              'Mix variado',
              Icons.shuffle,
              AppTheme.secondaryColor,
              PlaylistType.diverse,
              fullWidth: true,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaylistButton(
    String title,
    String subtitle,
    IconData icon,
    Color color,
    PlaylistType type, {
    bool fullWidth = false,
  }) {
    return BlocListener<PlaylistBloc, PlaylistState>(
      listener: (context, state) {
        if (state is PlaylistLoaded) {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => PlaylistPage(playlist: state.playlist),
            ),
          );
        } else if (state is PlaylistError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(state.message),
              backgroundColor: AppTheme.errorColor,
            ),
          );
        }
      },
      child: ElevatedButton(
        onPressed: () {
          context.read<PlaylistBloc>().add(
                CreatePlaylistEvent(
                  songId: widget.song.id,
                  type: type,
                  length: type == PlaylistType.optimal ? 6 : 10,
                ),
              );
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          padding: const EdgeInsets.all(16),
        ),
        child: Row(
          mainAxisSize: fullWidth ? MainAxisSize.max : MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon),
            const SizedBox(width: 8),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                Text(
                  subtitle,
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationsSection() {
    return BlocBuilder<RecommendationsBloc, RecommendationsState>(
      builder: (context, state) {
        if (state is RecommendationsLoading) {
          return const SliverToBoxAdapter(
            child: Center(
              child: Padding(
                padding: EdgeInsets.all(24.0),
                child: CircularProgressIndicator(),
              ),
            ),
          );
        }

        if (state is RecommendationsError) {
          return SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Text(
                'Error: ${state.message}',
                style: const TextStyle(color: AppTheme.errorColor),
              ),
            ),
          );
        }

        if (state is RecommendationsLoaded) {
          return SliverPadding(
            padding: const EdgeInsets.all(24),
            sliver: SliverList(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  if (index == 0) {
                    return Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: Text(
                        'Canciones Similares',
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                    );
                  }

                  final recommendation = state.recommendations[index - 1];
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: SongCard(
                      song: recommendation.song,
                      onTap: () {
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                SongDetailsPage(song: recommendation.song),
                          ),
                        );
                      },
                      trailing: Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: AppTheme.primaryColor.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          recommendation.similarityPercentage,
                          style: const TextStyle(
                            color: AppTheme.primaryColor,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  );
                },
                childCount: state.recommendations.length + 1,
              ),
            ),
          );
        }

        return const SliverToBoxAdapter(child: SizedBox.shrink());
      },
    );
  }
}
