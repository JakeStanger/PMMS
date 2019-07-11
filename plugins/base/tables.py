from database import db
import plugin_loader


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    api_key = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return "<%d - %s>" % (self.id, self.username)


plugin_loader.add_column('users', db.Column('test', db.String(64)))
plugin_loader.add_column('users', db.Column('test2', db.String(64)))
