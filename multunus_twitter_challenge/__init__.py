__author__ = 'ishaan'

from flask import Flask

app = Flask(__name__)
from multunus_twitter_challenge import views
