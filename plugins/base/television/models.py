from database import db


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    seasons = db.relationship('Season', back_populates='show')
    episodes = db.relationship('Episode', back_populates='show')


class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    number = db.Column(db.SmallInteger)

    show_key = db.Column(db.Integer, db.ForeignKey('shows.id'))

    show = db.relationship('Show', back_populates='seasons')
    episodes = db.relationship('Episode', back_populates='season')


class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    number = db.Column(db.SmallInteger)

    path = db.Column(db.Text, unique=True)
    duration = db.Column(db.BigInteger)
    size = db.Column(db.BigInteger)
    format = db.Column(db.String(32))

    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    show_key = db.Column(db.Integer, db.ForeignKey('shows.id'))
    season_key = db.Column(db.Integer, db.ForeignKey('seasons.id'))

    show = db.relationship('Show', back_populates='episodes')
    season = db.relationship('Season', back_populates='episodes')
