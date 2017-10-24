from app import db
# db from SQLAlchemy(app)


class BaseDB(db.Model):
    # flask_sqlalchemy aware of inheritance
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_mod = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())


class User(BaseDB):
    # id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(190), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(BaseDB):
    # id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    # timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Post: %r>' % (self.body)
