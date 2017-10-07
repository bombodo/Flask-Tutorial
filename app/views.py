from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'xD1337haxor'}
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
    #render_template uses Jinja2 template engine
    #applied to the template file found in the app/templates folder
    return render_template('index.html',
                            title='Wowzers',
                            memer=user,
                            posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # for debugging
        flash('Login requested for OpenID="%s", remember_me="%s"'%
                (form.openid, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                            title='Sign In',
                            form=form)
