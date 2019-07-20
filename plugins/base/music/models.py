from database import db


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    # albums: list = db.relationship('Album', back_populates='artist')
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
    album_artist_key = db.Column(db.Integer, db.ForeignKey('artists.id'))

    release_date = db.Column(db.Date)

    artist = db.relationship('Artist', backref='albums', foreign_keys=[artist_key])
    album_artist = db.relationship('Artist', foreign_keys=[album_artist_key])

    tracks: list = db.relationship('Track', back_populates='album', lazy='dynamic')
    genres: list = db.relationship('Genre', secondary=album_genre, back_populates='albums')

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

    album_key = db.Column(db.Integer, db.ForeignKey('albums.id'))

    duration = db.Column(db.BigInteger)

    track_num = db.Column(db.SmallInteger)
    disc_num = db.Column(db.SmallInteger)
    disc_name = db.Column(db.Text)

    path = db.Column(db.Text)
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