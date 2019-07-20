from database import db


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text, nullable=False)
    name_sort = db.Column(db.Text)

    path = db.Column(db.Text, unique=True)
    release_date = db.Column(db.Date)
    duration = db.Column(db.BigInteger)
    size = db.Column(db.BigInteger)
    format = db.Column(db.String(32))

    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
