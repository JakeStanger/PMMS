import plugin_loader
import server
from flask import render_template, redirect, url_for
from plugins.base.users import login_manager

login_manager.login_view = 'ui_static.login'

ui = plugin_loader.create_blueprint('ui_static', '/ui', 'plugins.webui_static',
                                    template_folder='plugins/webui_static/templates',
                                    static_folder='plugins/webui_static/static')


@server.app.route('/')
def app_index():
    return redirect(url_for('ui_static.index'))


@ui.route('/')
def index():
    return render_template('index.html', title='Home')


@ui.route('/login')
def login():
    return render_template('login.html', title='Login')


@ui.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')