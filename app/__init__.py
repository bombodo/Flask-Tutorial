from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
app.config.from_object('config')  # reads config file
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth2Provider(app)

from app import views, models
# views for base code on what user sees
# models for database model
