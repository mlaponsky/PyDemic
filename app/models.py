from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True, unique=True)
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
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(140), nullable=False, unique=True)
    game = db.Column(db.PickleType)
    actions = db.Column(db.PickleType)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
