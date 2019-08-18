import time

from flask import render_template, redirect, url_for
from flask_login import login_required
from plugins.webui_static.routes import ui
import database
from plugins.base.movies.models import Movie


@ui.route('/movies')
def movies():
    movie_list = database.db.session.query(Movie).all()

    render_data = [{'name': movie.name,
                    'release date': movie.release_date,
                    'duration': time.strftime('%H:%M:%S', time.gmtime(movie.duration / 1000)),
                    'id': movie.id,
                    'name_sort': movie.name_sort}
                   for movie in movie_list]
    render_data.sort(key=lambda artist: artist['name_sort'])

    return render_template('table.html',
                           headers=['name',
                                    {'name': 'release date', 'width': '0.25fr'},
                                    {'name': 'duration', 'width': '0.25fr'}],
                           data=render_data,
                           title='Movies')
