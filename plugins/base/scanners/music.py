import os
import re
from typing import List

from flask import jsonify
from mutagen import File
import database

import settings
import server
from plugins.base.tables import Album, Artist, Track, Genre
from datetime import datetime

settings.register_key('plugins.base.music.path', os.path.expanduser('~/Music'))


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


def get_name_sort(name: str):
    if not name:
        return None
    return re.match('(?:The |A )?(.*)', name)[1]


def get_artist_name(tags: File):
    return get_tag(tags, ['TPE1', 'artist', '\xa9ART'])


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


def get_album(name: str, release_date: datetime, genres: List[Genre], artist: Artist):
    if not name:
        return None

    album = database.db.session.query(Album).filter_by(name=name).first()
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
                      artist=artist)

        database.db.session.add(album)
        return album


def get_duration(tags: File):
    return tags.info.length


def get_track_num(tags: File):
    return get_tag(tags, ['TRCK', 'tracknumber', 'trkn'])


def get_disc_num(tags: File):
    return get_tag(tags, ['TXXX:CDNUMBER', 'discnumber', 'disk'])


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


@server.app.route('/import')
def import_music():
    music_path = os.path.expanduser(settings.get_key('plugins.base.music.path'))

    total_num = len([*os.walk(music_path)])
    num = 0

    for root, dirs, files in os.walk(music_path):
        num += 1
        for file in files:
            print('[%r%%] %s' % (round((num / total_num) * 100, 1), os.path.join(root, file)))
            tags = File(os.path.join(root, file))

            if tags is None:
                continue

            name = get_name(tags)
            name_sort = get_name_sort(name)

            artist = get_artist(get_artist_name(tags))
            album = get_album(get_album_name(tags), get_release_date(tags), get_genres(tags), artist)

            duration = get_duration(tags)

            track_num = get_track_num(tags)
            disc_num = get_disc_num(tags)
            disc_name = get_disc_name(tags)

            path = os.path.join(music_path, file)
            format = file.split('.')[-1]
            size = os.path.getsize(os.path.join(root, file))
            bitrate = tags.info.bitrate

            track = Track(name=name,
                          name_sort=name_sort,
                          artist=artist,
                          album=album,
                          duration=duration,
                          track_num=track_num,
                          disc_num=disc_num,
                          disc_name=disc_name,
                          path=path,
                          format=format,
                          bitrate=bitrate,
                          size=size)

            database.db.session.add(track)

    database.db.session.commit()
    return jsonify({'message': 'Import successful'}), 201
