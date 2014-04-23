__author__ = 'ishaan'

from multunus_twitter_challenge import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    screen_name = db.Column(db.String(64), index=True, unique=True)
    profile_image_url = db.Column(db.String(500))
    tweet_url = db.Column(db.String(500))
    tweet_id = db.Column(db.String(50))
    tweet_text = db.Column(db.String(200))
    tweet_data = db.Column(db.String(2000))
    last_updated = db.Column(db.DateTime)
    etag = db.Column(db.String(40))

    def __repr__(self):
        return '<User %r>' % self.screen_name