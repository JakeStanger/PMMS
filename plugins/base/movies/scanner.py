import os
import re
from typing import List

import settings
import server
import database
from flask import jsonify
from .models import Movie
from pymediainfo import MediaInfo
from datetime import datetime
from plugins.base.utils import get_name_sort


def get_name_and_release(path: List[str]):
    matches = re.match(r'(.+?)(?:(?:\((\d{4})\))|(?:\..{3}$|$))', path[0])

    if len(matches.groups()) < 2:
        return matches[0], None
    else:
        return matches.groups()


def import_movie(path: str, movie: Movie = None):
    movies_path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))
    relative_path = path.replace('%s/' % movies_path, '')
    path_split = relative_path.split('/')

    media_info = MediaInfo.parse(path)

    tracks = [track for track in media_info.tracks if track.track_type == 'Video']
    if not len(tracks):
        return

    for track in tracks:
        name, release = get_name_and_release(path_split)
        if release:
            release = release.replace('(', '').replace(')', '')
            release = datetime.strptime(release, '%Y')

        add = False
        if not movie:
            movie = Movie()
            add = True

        name = name.strip()

        movie.name = name
        movie.name_sort = get_name_sort(name)
        movie.path = relative_path
        movie.release_date = release
        movie.duration = track.duration
        movie.size = os.path.getsize(path)
        movie.format = track.format
        movie.width = track.width
        movie.height = track.height

        if add:
            database.db.session.add(movie)


@server.app.route('/import/movies', methods=['POST'])
def import_movies():
    movies_path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))

    for root, dirs, files in os.walk(movies_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = full_path.replace('%s/' % movies_path, '')

            print(relative_path)

            import_movie(full_path)

    database.db.session.commit()

    return jsonify({'message': 'Import successful'}), 201
