import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../../domain/entities/playlist.dart';
import '../../../config/theme/app_theme.dart';
import '../../widgets/song_card.dart';
import '../song_details/song_details_page.dart';

class PlaylistPage extends StatelessWidget {
  final Playlist playlist;

  const PlaylistPage({super.key, required this.playlist});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          _buildAppBar(context),
          _buildPlaylistInfo(context),
          _buildSongsList(context),
        ],
      ),
    );
  }

  Widget _buildAppBar(BuildContext context) {
    return SliverAppBar(
      expandedHeight: 250,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        background: Stack(
          fit: StackFit.expand,
          children: [
            if (playlist.songs.isNotEmpty)
              CachedNetworkImage(
                imageUrl: playlist.songs.first.coverUrl,
                fit: BoxFit.cover,
              ),
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.transparent,
                    AppTheme.backgroundColor.withOpacity(0.7),
                    AppTheme.backgroundColor,
                  ],
                ),
              ),
            ),
            Positioned(
              bottom: 16,
              left: 16,
              right: 16,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: _getAlgorithmColor(),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      playlist.algorithmDisplayName,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPlaylistInfo(BuildContext context) {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Playlist Generada',
              style: Theme.of(context).textTheme.displaySmall,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                _buildStatCard(
                  context,
                  Icons.music_note,
                  '${playlist.songs.length}',
                  'Canciones',
                ),
                const SizedBox(width: 12),
                _buildStatCard(
                  context,
                  Icons.timer,
                  playlist.totalDurationFormatted,
                  'Duración',
                ),
                const SizedBox(width: 12),
                _buildStatCard(
                  context,
                  Icons.auto_awesome,
                  '${(playlist.totalSimilarity * 100).toStringAsFixed(0)}%',
                  'Similitud',
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Divider(),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(
      BuildContext context, IconData icon, String value, String label) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppTheme.surfaceColor,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Icon(icon, color: AppTheme.primaryColor, size: 24),
            const SizedBox(height: 8),
            Text(
              value,
              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: Theme.of(context).textTheme.bodySmall,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSongsList(BuildContext context) {
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: 24),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) {
            if (index == 0) {
              return Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Text(
                  'Canciones',
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
              );
            }

            final song = playlist.songs[index - 1];
            return Padding(
              padding: const EdgeInsets.only(bottom: 12),
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
                trailing: Container(
                  width: 32,
                  height: 32,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor.withOpacity(0.2),
                    shape: BoxShape.circle,
                  ),
                  child: Center(
                    child: Text(
                      '${index}',
                      style: const TextStyle(
                        color: AppTheme.primaryColor,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
              ),
            );
          },
          childCount: playlist.songs.length + 1,
        ),
      ),
    );
  }

  Color _getAlgorithmColor() {
    switch (playlist.algorithmUsed.toLowerCase()) {
      case 'backtracking':
        return AppTheme.primaryColor;
      case 'greedy':
        return AppTheme.accentColor;
      case 'diverse_backtracking':
        return AppTheme.secondaryColor;
      default:
        return AppTheme.primaryColor;
    }
  }
}
