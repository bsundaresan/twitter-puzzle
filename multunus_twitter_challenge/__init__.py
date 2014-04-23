__author__ = 'ishaan'

from flask import Flask
from config import DATABASE_URL
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
from multunus_twitter_challenge import views, models
