import os
import re
from typing import List

import settings
import server
import database
from flask import jsonify
from plugins.base.tables import Movie
from pymediainfo import MediaInfo
from datetime import datetime
from .utils import get_name_sort

settings.register_key('plugins.base.movies.path', os.path.expanduser('~/Movies'))


def get_name_and_release(path: List[str]):
    matches = re.match(r'(.+?)(?:(?:\((\d{4})\))|(?:\..{3}$|$))', path[0])

    if len(matches.groups()) < 2:
        return matches[0], None
    else:
        return matches.groups()


@server.app.route('/import/movies', methods=['POST'])
def import_movies():
    movies_path = os.path.expanduser(settings.get_key('plugins.base.movies.path'))

    for root, dirs, files in os.walk(movies_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = full_path.replace('%s/' % movies_path, '')
            path_split = relative_path.split('/')

            # print(relative_path)
            print(relative_path)

            media_info = MediaInfo.parse(full_path)

            tracks = [track for track in media_info.tracks if track.track_type == 'Video']
            if not len(tracks):
                continue

            for track in tracks:
                name, release = get_name_and_release(path_split)
                if release:
                    release = release.replace('(', '').replace(')', '')
                    release = datetime.strptime(release, '%Y')

                movie = Movie(name=name,
                              name_sort=get_name_sort(name),
                              path=relative_path,
                              release_date=release,
                              duration=track.duration,
                              size=os.path.getsize(full_path),
                              format=track.format,
                              width=track.width,
                              height=track.height)

                database.db.session.add(movie)

    database.db.session.commit()

    return jsonify({'message': 'Import successful'}), 201
