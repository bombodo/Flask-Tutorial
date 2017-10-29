from app import db
from passlib.hash import pbkdf2_sha256

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
    password = db.Column(db.String(150), nullable=False)   # hash with PBKDF2
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    oauth_client = db.relationship('Client', backref='user', lazy='dynamic')
    token = db.relationship('Token', backref='user', lazy='dynamic')
    # post.author refers 'BACK' to this table
    # client.user, etc etc

    def check_password(self, password):
        pwhash = pbkdf2_sha256.hash("password")
        return pwhash == self.password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)


class Post(BaseDB):
    # id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    # timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post: %r>' % (self.body)


class Client(db.Model):
    # TODO: find what size id and secrets should be
    client_id = db.Column(db.String(60), primary_key=True)
    client_secret = db.Column(db.String(60), unique=True, index=True,
                              nullable=False)
    is_confidential = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.relationship('Token', backref='client', lazy='dynamic')

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_mod = db.Column(db.DateTime, default=db.func.current_timestamp(),
                         onupdate=db.func.current_timestamp())

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_id = db.Column(db.String(60), db.ForeignKey('client.client_id'),
                          nullable=False)
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
