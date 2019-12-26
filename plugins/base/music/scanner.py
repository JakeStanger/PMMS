import os
import re
from typing import List

from flask import jsonify
from mutagen import File
import database

import settings
import server
from .models import Album, Artist, Track, Genre
from datetime import datetime
from plugins.base.utils import get_name_sort


def get_tag(tags: File, tag_names: List[str], get_all=False):
    for tag in tag_names:
        val = tags.get(tag)
        if val:
            if hasattr(val, 'text'):
                val = val.text

            if get_all:
                return val

            while type(val) == list or type(val) ==  tuple:
                val = val[0]
            return val


def get_name(tags: File):
    return get_tag(tags, ['TIT2', 'title', '\xa9nam'])


def get_artist_name(tags: File):
    return get_tag(tags, ['TPE1', 'artist', '\xa9ART'])


def get_album_artist_name(tags: File):
    return get_tag(tags, ['TPE2', 'albumartist', 'aART'])


def get_album_name(tags: File):
    return get_tag(tags, ['TALB', 'album', '\xa9alb'])


def get_genre(name: str):
    if not name:
        return None

    album = database.db.session.query(Genre).filter_by(name=name).first()
    if album:
        return album
    else:
        genre = Genre(name=name)
        database.db.session.add(genre)
        return genre


def get_artist(name: str):
    if not name:
        return None

    album = database.db.session.query(Artist).filter_by(name=name).first()
    if album:
        return album
    else:
        artist = Artist(name=name, name_sort=get_name_sort(name))
        database.db.session.add(artist)
        return artist


def get_album(name: str, release_date: datetime, genres: List[Genre], artist: Artist, album_artist: Artist):
    if not name:
        return None

    album = database.db.session.query(Album).filter_by(name=name, artist=artist).first()
    if album:
        if genres:
            existing = [genre.name for genre in album.genres]
            for genre in genres:
                if genre.name not in existing:
                    album.genres.append(genre)
        return album
    else:
        album = Album(name=name,
                      name_sort=get_name_sort(name),
                      release_date=release_date,
                      genres=genres,
                      artist=artist,
                      album_artist=album_artist)

        database.db.session.add(album)
        return album


def get_duration(tags: File):
    return tags.info.length


def get_track_num(tags: File):
    track_num = get_tag(tags, ['TRCK', 'tracknumber', 'trkn'])

    if not track_num:
        return None

    if '/' in track_num:
        return track_num.split('/')[0]
    return track_num


def get_disc_num(tags: File):
    disc_num = get_tag(tags, ['TXXX:CDNUMBER', 'discnumber', 'disk'])

    if not disc_num:
        return None

    if '/' in disc_num:
        return disc_num.split('/')[0]
    return disc_num


def get_disc_name(tags: File):
    return get_tag(tags, ['TXXX:TSST', 'tsst'])


def get_release_date(tags: File):
    date: str = get_tag(tags, ['TDRC', 'date'])

    if not date:
        return

    if type(date) is not str:
        date = str(date)

    if not len(date):
        return

    if re.match(r'^\d{4}$', date):
        return datetime.strptime(date, '%Y')
    else:
        return datetime.strptime(date, '%Y-%m-%d')


def get_genres(tags: File):
    genres = get_tag(tags, ['TCON', 'genres'], get_all=True) or []
    return [get_genre(genre) for genre in genres]


def import_track(full_path: str, track: Track = None):
    music_path = os.path.expanduser(settings.get_key('plugins.base.music.path'))

    tags = File(full_path)

    if tags is None:
        return

    relative_path = full_path.replace('%s/' % music_path, '')

    name = get_name(tags)
    name_sort = get_name_sort(name)

    artist = get_artist(get_artist_name(tags))
    album_artist = get_artist(get_album_artist_name(tags))
    album = get_album(get_album_name(tags), get_release_date(tags), get_genres(tags), artist, album_artist)

    duration = get_duration(tags)

    track_num = get_track_num(tags)
    disc_num = get_disc_num(tags)
    disc_name = get_disc_name(tags)

    format = relative_path.split('.')[-1]
    size = os.path.getsize(full_path)
    bitrate = tags.info.bitrate

    add = False
    if track is None:
        track = Track()
        add = True

    track.name = name
    track.name_sort = name_sort
    track.artist = artist
    track.album = album
    track.duration = duration
    track.track_num = track_num
    track.disc_num = disc_num
    track.disc_name = disc_name
    track.path = relative_path
    track.format = format
    track.bitrate = bitrate
    track.size = size

    if add:
        database.db.session.add(track)


@server.app.route('/import/music', methods=['POST'])
def import_music():
    music_path = os.path.expanduser(settings.get_key('plugins.base.music.path'))

    total_num = len([*os.walk(music_path)])
    num = 0

    for root, dirs, files in os.walk(music_path):
        num += 1
        for file in files:
            print('[%r%%] %s' % (round((num / total_num) * 100, 1), os.path.join(root, file)))

            import_track(os.path.join(root, file))

    database.db.session.commit()
    return jsonify({'message': 'Import successful'}), 201
