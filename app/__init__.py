from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config') #reads config file
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views, models
#views for base code on what user sees
#models for database model
