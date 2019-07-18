import os
import re
import server
import database
import settings
from flask import jsonify
from plugins.base.tables import Show, Season, Episode
from .utils import get_name_sort
from pymediainfo import MediaInfo

settings.register_key('plugins.base.tv.path', os.path.expanduser('~/Television'))

def get_show(show_name: str):
    if not show_name:
        return None

    show = database.db.session.query(Show).filter_by(name=show_name).first()
    if show:
        return show
    else:
        show = Show(name=show_name, name_sort=get_name_sort(show_name))
        database.db.session.add(show)
        return show


def get_season(season_name: str, season_num: int, show: Show):
    if not season_name:
        return None

    season = database.db.session.query(Season).filter_by(name=season_name).first()
    if season:
        return season
    else:
        season = Season(name=season_name, name_sort=get_name_sort(season_name), number=season_num, show=show)
        database.db.session.add(season)
        return season


def get_details_from_filename(filename: str):
    matches = re.match(r'{?(.*) - S(\d{2,})E(\d{2,})(?:-\d{2})? - ([^.]*)',
                       filename)

    return matches.groups()


@server.app.route('/import/tv', methods=['POST'])
def import_tv():
    tv_path = os.path.expanduser(settings.get_key('plugins.base.tv.path'))

    for root, dirs, files in os.walk(tv_path):
        for file in files:
            show_name, season_num, episode_num, episode_name = get_details_from_filename(file)

            full_path = os.path.join(root, file)

            relative_path = full_path.replace('%s/' % tv_path, '')
            print(relative_path)

            media_info = MediaInfo.parse(full_path)

            tracks = [track for track in media_info.tracks if track.track_type == 'Video']
            if not len(tracks):
                continue

            for track in tracks:
                show = get_show(show_name)
                season = get_season('Season %r' % season_num, season_num, show)

                episode = Episode(
                    name=episode_name,
                    name_sort=get_name_sort(episode_name),
                    number=episode_num,
                    duration=track.duration,
                    size=os.path.getsize(full_path),
                    format=track.format,
                    width=track.width,
                    height=track.height,
                    show=show,
                    season=season,
                )

                database.db.session.add(episode)

    database.db.session.commit()

    return jsonify({'message': 'Import successful'}), 201
