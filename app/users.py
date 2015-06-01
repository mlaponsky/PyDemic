from app import db
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user

def are_equal(x, y):
    return x==y

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    game_id = db.Column(db.String(120), nullable=True, unique=True)
    games = db.relationship('GameStore', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class GameStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(140), nullable=False, unique=True)
    data = db.Column(db.PickleType)
    action = db.relationship('Action', backref='author', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(140), db.ForeignKey('game.game_id'))
    phase = db.Column(db.Integer, nullable=False)
    turn = db.Column(db.Integer, nullable=False)
    active = db.Column(db.String(64), nullable=True)
    mover = db.Column(db.String(64), nullable=True)
    owner = db.Column(db.String(64), nullable=True)
