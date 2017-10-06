from flask import Flask

app = Flask(__name__)
app.config.from_object('config') #reads config file

from app import views
