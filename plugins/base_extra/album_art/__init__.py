from io import BytesIO

from flask import jsonify
from sqlalchemy.orm.exc import NoResultFound

from .local import fetch_local_art
from .lastfm import fetch_lastfm_art
from .musicbrainz import fetch_musicbrainz_art


def init():
    import settings
    import server
    import database

    settings.register_key('plugins.base_extra.music.album_art.enable', True)
    settings.register_key('plugins.base_extra.music.album_art.local.enable', True)

    settings.register_key('plugins.base_extra.music.album_art.lastfm.enable', False)
    settings.register_key('plugins.base_extra.music.album_art.lastfm.api_key', '')

    settings.register_key('plugins.base_extra.music.album_art.musicbrainz.enable', False)

    settings.register_key('plugins.base_extra.music.album_art.cache.enable', True)
    settings.register_key('plugins.base_extra.music.album_art.cache.path', '~/.cache/pmms/albumart')

    if settings.get_key('plugins.base_extra.music.album_art.enable'):
        from plugins.base.music.models import Album
        from flask import send_file
        import os

        def load_cache(album: Album):
            cache_path = os.path.expanduser(settings.get_key('plugins.base_extra.music.album_art.cache.path'))
            full_path = os.path.join(cache_path,  '%s - %s.jpg' % (album.artist.name, album.name))
            if os.path.isfile(full_path):
                with open(full_path, 'rb') as f:
                    return BytesIO(f.read())

        def write_cache(art: BytesIO, album: Album):
            cache_path = os.path.expanduser(settings.get_key('plugins.base_extra.music.album_art.cache.path'))
            if not os.path.isdir(cache_path):
                os.makedirs(cache_path)

            with open(os.path.join(cache_path, '%s - %s.jpg' % (album.artist.name, album.name)), 'wb') as f:
                f.write(art.read())

        @server.app.route('/api/artists/<int:_artist_id>/albums/<int:album_id>/art')
        @server.app.route('/api/albums/<int:album_id>/art')
        def get_album_art(album_id: int, _artist_id: int = None):
            try:
                album = database.db.session.query(Album).filter_by(id=album_id).one()
            except NoResultFound:
                return jsonify({'message': 'Album does not exist'}), 404

            art = None

            enable_cache = settings.get_key('plugins.base_extra.music.album_art.cache.enable')

            if enable_cache:
                art = load_cache(album)

            do_cache = True
            if art:
                do_cache = False

            if not art and settings.get_key('plugins.base_extra.music.album_art.local.enable'):
                art = fetch_local_art(album)
            if not art and settings.get_key('plugins.base_extra.music.album_art.musicbrainz.enable'):
                art = fetch_musicbrainz_art(album)
            if not art and settings.get_key('plugins.base_extra.music.album_art.lastfm.enable'):
                art = fetch_lastfm_art(album)

            if art:
                if enable_cache and do_cache:
                    write_cache(art, album)

                art.seek(0)  # Writing to cache moves stream pos to end

                return send_file(art, mimetype='image/jpeg')
            else:
                return jsonify({'message': 'Failed to find art'}), 404

        if settings.get_key('plugins.base_extra.music.album_art.musicbrainz.enable'):
            import musicbrainzngs as mb
            mb.set_useragent('pmms', '1.0.0')
