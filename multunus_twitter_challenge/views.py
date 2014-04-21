__author__ = 'ishaan'

from multunus_twitter_challenge import app
from flask import render_template
from models import User

handles = []
handle_data = []


@app.route('/', methods=['GET'])
def home():
    try:
        users = User.query.all()
    except Exception as e:
        print e
        return "Something went wrong"
    else:
        return render_template('index.html', data=users)


@app.route('/<id>', methods=['GET'])
def rank_page(id):
    return id

