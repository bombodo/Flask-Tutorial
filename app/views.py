from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
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


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'xD1337haxor'}
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = {'nickname': 'xD1337haxor'}
    form = LoginForm()
    if form.validate_on_submit():
        # for debugging
        flash('Login requested for OpenID="%s", remember_me="%s"' %
              (form.openid, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           memer=user,
                           form=form)
