from database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
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