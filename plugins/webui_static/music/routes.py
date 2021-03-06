import datetime
import time
from typing import Optional

from flask import render_template, redirect, url_for, request

import database
import plugin_loader
from plugins.base.music.models import Artist, Album, Track
from plugins.webui_static.routes import ui


@ui.route('/music')
def music_index():
    return redirect(url_for('ui_static.artists'))


@ui.route('/music/artists')
# @login_required
def artists():
    artist_list = database.db.session.query(Artist).all()

    render_data = [{'name': artist.name,
                    'count': len(artist.albums),
                    'id': artist.id,
                    'name_sort': artist.name_sort}
                   for artist in artist_list if len(artist.albums) > 0]
    render_data.sort(key=lambda artist: artist['name_sort'])

    return render_template('table.html',
                           headers=['name', 'count'],
                           data=render_data,
                           link='ui_static.albums',
                           title='Music',
                           description='List of artists',
                           )


@ui.route('/music/artists/<int:key>')
# @login_required
def albums(key: int):
    album_list = database.db.session.query(Album).filter(Album.artist.has(id=key)).all()

    render_data = [{'name': album.name,
                    'released': album.release_date,
                    'count': len(album.tracks),
                    'id': album.id}
                   for album in album_list if len(album.tracks) > 0]

    render_data.sort(key=lambda album: album['released'] or datetime.date.fromtimestamp(-9999999999))

    artist_name = album_list[0].artist.name

    return render_template('table.html',
                           headers=['name', 'released', 'count'],
                           data=render_data,
                           link='ui_static.tracks',
                           title=artist_name,
                           description='Albums by %s on PMMS' % artist_name,
                           )


@ui.route('/music/albums/<int:key>')
# @login_required
def tracks(key: int):
    track_list = database.db.session.query(Track).filter(Track.album.has(id=key)).all()

    render_data = [{
        'name': track.name,
        'duration': time.strftime('%M:%S', time.gmtime(track.duration)),
        'track num': track.track_num if track.track_num else 0,
        'disc num': track.disc_num if track.disc_num else 1,
        'disc name': '%s / %s' % (track.disc_num, track.disc_name) if track.disc_name else 'Disc %s' % track.disc_num,
        'id': track.id
    }
        for track in track_list]

    render_data.sort(key=lambda track: (track['disc num'], track['track num']))

    album_name = track_list[0].album.name
    artist_name = track_list[0].artist.name

    image_url: Optional[str] = None
    if plugin_loader.is_module_loaded('base_extra'):
        image_url = request.url_root[:-1] + url_for('get_album_art', album_id=key)

    return render_template('table.html',
                           headers=[{'name': 'track num', 'width': '0.2fr'},
                                    {'name': 'name', 'width': '1.5fr'},
                                    'duration'],
                           data=render_data,
                           group='disc name',
                           title=album_name,
                           description='Tracks from %s by %s' % (album_name, artist_name),
                           image=image_url,
                           link='ui_static.track')


@ui.route('/music/tracks/<int:key>')
def track(key: int):
    track = database.db.session.query(Track).filter_by(id=key).one()

    lyrics: Optional[str] = None
    image_url: Optional[str] = None
    if plugin_loader.is_module_loaded('base_extra'):
        from plugins.base_extra.lyrics import get_lyrics

        lyrics = get_lyrics(track.id)
        image_url = request.url_root[:-1] + url_for('get_album_art', album_id=track.album.id)

    return render_template('track.html',
                           track=track,
                           lyrics=lyrics,
                           title=track.name,
                           description='%s from %s by %s' % (track.name, track.album.name, track.artist.name),
                           image=image_url)
