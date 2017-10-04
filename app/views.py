from flask import render_template
from app import app

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
