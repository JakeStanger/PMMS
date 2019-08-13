from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

def init():
    import settings
    import server
    import database

    settings.register_key('plugins.base_extra.music.lyrics.enable', True)

    settings.register_key('plugins.base_extra.music.lyrics.cache.enable', True)
    settings.register_key('plugins.base_extra.music.lyrics.cache.path', '~/.cache/pmms/lyrics')

    settings.register_key('plugins.base_extra.music.lyrics.genius.enable', False)
    settings.register_key('plugins.base_extra.music.lyrics.genius.api_key', '')

    if settings.get_key('plugins.base_extra.music.lyrics.enable'):
        from plugins.base.music.models import Track
        from .genius import fetch_genius_lyrics
        import os

        def load_cache(track: Track):
            cache_path = os.path.expanduser(settings.get_key('plugins.base_extra.music.lyrics.cache.path'))
            full_path = os.path.join(cache_path,  '%s - %s.txt' % (track.artist.name, track.name))

            if os.path.isfile(full_path):
                with open(full_path, 'r') as f:
                    return f.read()


        def write_cache(lyrics: str, track: Track):
            cache_path = os.path.expanduser(settings.get_key('plugins.base_extra.music.lyrics.cache.path'))
            full_path = os.path.join(cache_path, '%s - %s.txt' % (track.artist.name, track.name))

            if not os.path.isdir(cache_path):
                os.makedirs(cache_path)

            with open(full_path, 'w') as f:
                f.write(lyrics)

        @server.app.route('/api/albums/<int:_album_id>/tracks/<int:track_id>/lyrics')
        @server.app.route('/api/tracks/<int:track_id>/lyrics')
        def get_lyrics(track_id: int, _album_id: int = None):
            try:
                track = database.db.session.query(Track).filter_by(id=track_id).one()
            except NoResultFound:
                return jsonify({'message': 'Track does not exist'}), 404

            lyrics = None
            enable_cache = settings.get_key('plugins.base_extra.music.lyrics.cache.enable')

            if enable_cache:
                lyrics = load_cache(track)

            do_cache = True
            if lyrics:
                do_cache = False

            if not lyrics and settings.get_key('plugins.base_extra.music.lyrics.genius.enable'):
                lyrics = fetch_genius_lyrics(track)

            if lyrics:
                if enable_cache and do_cache:
                    write_cache(lyrics, track)

                return jsonify({'lyrics': lyrics})
            else:
                return jsonify({'message': 'Failed to find lyrics'}), 404
