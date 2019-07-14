from database import db
from flask_login import UserMixin
import plugin_loader


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    api_key = db.Column(db.String(64), nullable=True)

    playlists = db.relationship('Playlist', back_populates='creator')

    def __repr__(self):
        return "<User:%d - %s>" % (self.id, self.username)


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    album_count = db.Column(db.SmallInteger)

    albums: list = db.relationship('Album', back_populates='artist')
    tracks: list = db.relationship('Track', back_populates='artist')

    def __repr__(self):
        return "<Artist:%d - %s>" % (self.id, self.name)


album_genre = db.Table('album_genre',
                       db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
                       db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True))


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    artist_key = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist_name = db.Column(db.Text)

    release_date = db.Column(db.Date)

    track_count = db.Column(db.SmallInteger)

    artist = db.relationship('Artist', back_populates='albums')
    tracks: list = db.relationship('Track', back_populates='album')
    genres = db.relationship('Genre', secondary=album_genre, back_populates='albums')

    def __repr__(self):
        return "<Album:%d - %s>" % (self.id, self.name)


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    albums = db.relationship('Album', secondary=album_genre, back_populates='genres')

    def __repr__(self):
        return "<Genre:%d - %s>" % (self.id, self.name)


playlist_track = db.Table('playlist_track',
                          db.Column('track_id', db.Integer, db.ForeignKey('tracks.id'), primary_key=True),
                          db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id'), primary_key=True))


class Track(db.Model):
    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    artist_key = db.Column(db.Integer, db.ForeignKey('artists.id'))
    artist_name = db.Column(db.Text)

    album_key = db.Column(db.Integer, db.ForeignKey('albums.id'))
    album_name = db.Column(db.Text)

    duration = db.Column(db.BigInteger)

    track_num = db.Column(db.SmallInteger)
    disc_num = db.Column(db.SmallInteger)

    download_url = db.Column(db.Text)
    bitrate = db.Column(db.Integer)
    size = db.Column(db.BigInteger)
    format = db.Column(db.String(32))

    artist = db.relationship('Artist', back_populates='tracks')
    album = db.relationship('Album', back_populates='tracks')

    playlists = db.relationship('Playlist', secondary=playlist_track, back_populates='tracks')

    def __repr__(self):
        return "<Track:%d - %s>" % (self.id, self.name)


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    creator = db.relationship('User', back_populates='playlists')
    tracks = db .relationship('Track', secondary=playlist_track, back_populates='playlists')

    def __repr__(self):
        return "<Playlist:%d - %s>" % (self.id, self.name)


plugin_loader.add_api_endpoints(Artist, ['GET'])
plugin_loader.add_api_endpoints(Album, ['GET'])
plugin_loader.add_api_endpoints(Track, ['GET'])
plugin_loader.add_api_endpoints(Genre, ['GET'])
plugin_loader.add_api_endpoints(Playlist, ['GET'])
