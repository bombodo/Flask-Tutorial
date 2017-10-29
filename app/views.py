from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oauth
from datetime import datetime  # , timedelta
from .forms import LoginForm
from .models import User, Client, Token
from flask_oauthlib.contrib.oauth2 import bind_sqlalchemy
from flask_oauthlib.contrib.oauth2 import bind_cache_grant
# from flask_oauth import OAuth

# oauth = OAuth()
#
# google = oauth.remote_app('google',
#     base_url='https://www.google.com/accounts/',
#     request_token_url=None,
#     access_token_url='https://www.google.com/o/oauth2/token',
#     access_token_method='POST',
#     access_token_params={'grant_type': 'authorization_code'},
#     consumer_key=GOOGLE_CLIENT_ID,
#     consumer_secret=GOOGLE_CLIENT_SECRET
#     )

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
    # user = ?
    # TODO: g.user = ? read documentation for flask-login manager


bind_sqlalchemy(oauth, db.session, user=User,
                token=Token, client=Client)
app.config.update({'OAUTH2_CACHE_TYPE': 'simple'})  # need to move to config.py
# bind_cache_grant(app, oauth, g.user)  # need to read into params and config


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    user = g.user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    # render_template uses Jinja2 template engine
    # applied to the template file found in the app/templates folder
    return render_template('index.html',
                           title='Wowzers',
                           memer=user,
                           posts=posts)



# @oauth.grantgetter  # need clarification
# def load_grant(client_id, code):
#
#
# @oauth.grantsetter  # need clarification
# def set_grant(client_id, code, request, *args, **kwargs):
#     expires = datetime.utcnow() + timedelta(days=2)
#     grant = Grant(client_id=client_id,
#                   code=code['code'])
#
# @oauth.tokengetter
# def load_token(access_token=None, refresh_token=None):
#     if access_token:
#         return Token.query.filter_by(access_token=access_token)
#
# @oauth.tokensetter
# def save_token(token, request, *args, **kwargs):
#     toks = Token.query.filter_by(client_id=request.client.client_id,
#                                  user=request.user.id)
#
#     for t in toks:  # remove prior tokens so only one exists
#         db.session.delete(t)
#
#     expires_in = token.get('expires_in')  # how do we ensure seconds?
#     expires = datetime.utcnow() + timedelta(seconds=expires_in)
#
#     tok = Token(
#         access_token=token['access_token'],
#         refresh_token=token['refresh_token'],
#         token_type=token['token_type'],
#         _scopes=token['scope'],
#         expires=expires,
#         client_id=request.client.client_id,
#         user_id=request.user.id
#     )
#     db.session.add(tok)
#     db.session.commit()
#     return tok



@app.route('/login', methods=['GET','POST'])
def login():
    user = {'nickname': 'xD1337haxor'}
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # for debugging
        flash('Login requested for User="%s", remember_me="%s"' %
              (form.username, str(form.remember_me.data)))
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password):
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # session['remember_me'] = form.remember_me.data
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           memer=user,
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
