import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../domain/entities/song.dart';
import '../../config/theme/app_theme.dart';

class SongCard extends StatelessWidget {
  final Song song;
  final VoidCallback onTap;
  final Widget? trailing;

  const SongCard({
    super.key,
    required this.song,
    required this.onTap,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              _buildCover(),
              const SizedBox(width: 12),
              Expanded(
                child: _buildInfo(context),
              ),
              if (trailing != null) trailing!,
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCover() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: CachedNetworkImage(
        imageUrl: song.coverUrl,
        width: 64,
        height: 64,
        fit: BoxFit.cover,
        placeholder: (context, url) => Container(
          width: 64,
          height: 64,
          color: AppTheme.surfaceColor,
          child: const Icon(Icons.music_note, color: AppTheme.textTertiaryColor),
        ),
        errorWidget: (context, url, error) => Container(
          width: 64,
          height: 64,
          color: AppTheme.surfaceColor,
          child: const Icon(Icons.music_note, color: AppTheme.textTertiaryColor),
        ),
      ),
    );
  }

  Widget _buildInfo(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          song.title,
          style: Theme.of(context).textTheme.titleLarge,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        const SizedBox(height: 4),
        Text(
          song.artist,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppTheme.textSecondaryColor,
              ),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        const SizedBox(height: 4),
        Row(
          children: [
            const Icon(
              Icons.music_note,
              size: 14,
              color: AppTheme.textTertiaryColor,
            ),
            const SizedBox(width: 4),
            Text(
              song.genres.isNotEmpty ? song.genres.first : 'Unknown',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(width: 12),
            const Icon(
              Icons.timer,
              size: 14,
              color: AppTheme.textTertiaryColor,
            ),
            const SizedBox(width: 4),
            Text(
              song.durationFormatted,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ],
    );
  }
}
