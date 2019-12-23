from flask import request
from mpd import MPDClient
from fuzzywuzzy.process import extractOne

import plugin_loader
import settings

mpd_bp = plugin_loader.create_blueprint('mpd', '/mpd', 'plugins.mpd_webhooks')

settings_set = settings.SettingsSet('plugins.mpd_webhooks')


@mpd_bp.route('/album', methods=['POST'])
def queue_album():
    client = MPDClient()
    client.connect(settings_set.get_key('mpd_host'), settings_set.get_key('mpd_port'))

    data = request.data.decode('utf-8')

    album_query, artist_query = data.split(' by ')

    artists = client.list('artist')

    artist, artist_confidence = extractOne(artist_query,
                                           artists)

    albums = client.list('album', '(artist == \'%s\')' % artist)
    album, album_confidence = extractOne(album_query,
                                         albums)

    client.findadd("album", album, "artist", artist)

    client.play()

    return 'Success'
