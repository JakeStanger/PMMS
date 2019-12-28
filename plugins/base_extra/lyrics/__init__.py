from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from plugins.base.music.models import Track
from .genius import fetch_genius_lyrics
import os
import settings
import database

settings_set = settings.SettingsSet('plugins.base_extra.music.lyrics')


def load_cache(track: Track):
    cache_path = os.path.expanduser(settings_set.get_key('cache.path'))
    full_path = os.path.join(cache_path, '%s - %s.txt' % (track.artist.name, track.name))

    if os.path.isfile(full_path):
        with open(full_path, 'r') as f:
            return f.read()


def write_cache(lyrics: str, track: Track):
    cache_path = os.path.expanduser(settings_set.get_key('cache.path'))
    full_path = os.path.join(cache_path, '%s - %s.txt' % (track.artist.name, track.name))

    if not os.path.isdir(cache_path):
        os.makedirs(cache_path)

    with open(full_path, 'w') as f:
        f.write(lyrics)


def get_lyrics(track_id: int):
    try:
        track = database.db.session.query(Track).filter_by(id=track_id).one()
    except NoResultFound:
        return jsonify({'message': 'Track does not exist'}), 404

    lyrics = None
    enable_cache = settings_set.get_key('cache.enable')

    if enable_cache:
        lyrics = load_cache(track)

    do_cache = True
    if lyrics:
        do_cache = False

    if not lyrics and settings_set.get_key('genius.enable'):
        lyrics = fetch_genius_lyrics(track)

    if lyrics:
        if enable_cache and do_cache:
            write_cache(lyrics, track)

        return lyrics


def init():
    import server

    settings_set.register_key('enable', True)

    settings_set.register_key('cache.enable', True)
    settings_set.register_key('cache.path', '~/.cache/pmms/lyrics')

    settings_set.register_key('genius.enable', False)
    settings_set.register_key('genius.api_key', '')

    if settings_set.get_key('enable'):
        @server.app.route('/api/albums/<int:_album_id>/tracks/<int:track_id>/lyrics')
        @server.app.route('/api/tracks/<int:track_id>/lyrics')
        def lyrics(track_id: int, _album_id: int = None):
            lyrics = get_lyrics(track_id)

            if lyrics:
                return jsonify({'lyrics': lyrics})
            else:
                return jsonify({'message': 'Failed to find lyrics'}), 404

