__author__ = 'ishaan'

from multunus_twitter_challenge import app
from flask import render_template, abort, request, make_response
from models import User
import json
import hashlib

handles = []
handle_data = []



@app.route('/', methods=['GET'])
def home():
    etag = hashlib.sha1('asd').hexdigest()  # Assuming home page content will never change
    etag_from_browser = request.headers.get('If-None-Match')
    if etag_from_browser:
        etag_from_browser = etag_from_browser.replace('"', '')
        if etag_from_browser == etag:
            response = make_response("", 304)
            response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
            return response
    try:
        users = User.query.all()
        users.sort(key=lambda x: x.id)
    except Exception as e:
        print e
        return "Something went wrong"
    else:
        response = make_response(render_template('index.html', data=users))
        response.set_etag(etag)
        response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
        return response


@app.route('/<id>', methods=['GET'])
def rank_page(id):
    u = User.query.filter_by(id=id).first_or_404()
    etag = u.etag
    etag_from_browser = request.headers.get('If-None-Match')
    if etag_from_browser:
        etag_from_browser = etag_from_browser.replace('"', '')
        if etag_from_browser == etag:
            response = make_response("", 304)
            response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
            return response
    try:
        ranked_data = json.loads(u.tweet_data)
    except Exception as e:
        abort(500)
    else:
        response = make_response(render_template('rank.html', ranked_data=ranked_data, handle_data=u))
        response.set_etag(u.etag)
        response.headers['Cache-Control'] = 'max-age=0, private, must-revalidate'
        return response