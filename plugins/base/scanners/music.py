import os
import re
from typing import List

from flask import jsonify
from mutagen import File
import database

import settings
import server
from plugins.base.tables import Album, Artist, Track

settings.register_key('plugins.base.music.path', os.path.expanduser('~/Music'))


def get_tag(tags: File, tag_names: List[str]):
    for tag in tag_names:
        val = tags.get(tag)
        if val:
            if hasattr(val, 'text'):
                val = val.text

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


def get_album(name: str, artist: Artist):
    if not name:
        return None

    album = database.db.session.query(Album).filter_by(name=name).first()
    if album:
        return album
    else:
        album = Album(name=name, name_sort=get_name_sort(name), artist=artist)
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


@server.app.route('/import')
def import_music():
    music_path = os.path.expanduser(settings.get_key('plugins.base.music.path'))
    for root, dirs, files in os.walk(music_path):
        for file in files:
            print(os.path.join(root, file))
            tags = File(os.path.join(root, file))

            if tags is None:
                continue

            name = get_name(tags)
            name_sort = get_name_sort(name)

            artist = get_artist(get_artist_name(tags))
            album = get_album(get_album_name(tags), artist)

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
