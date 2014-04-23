__author__ = 'ishaan'

from multunus_twitter_challenge.models import User
from multunus_twitter_challenge import twitter_api
from multunus_twitter_challenge import db
import json
from datetime import datetime
import hashlib


def get_profile_images():
    data = User.query.all()
    for d in data:
        screen_name = d.screen_name
        user_info = twitter_api.get_user_info(screen_name=screen_name)
        if not user_info:
            continue
        image_url = user_info.get('profile_image_url')
        image_url = image_url.replace('_normal', '')
        d.profile_image_url = image_url
    db.session.commit()


def update(handle=None):
    if not handle:
        handles = User.query.all()
    else:
        handles = handle
    for h in handles:
        rt_ids = twitter_api.get_retweeters(h.tweet_id)
        if not rt_ids:
            continue
        rt_users = []
        counter = 0
        top_ten = []
        for l in rt_ids['ids']:
            if counter == 10:
                break
            if l not in top_ten:
                top_ten.append(l)
                counter += 1

        for user_id in top_ten:
            user_info = twitter_api.get_user_info(user_id=user_id)
            if user_info:
                rt_users.append(user_info)
        rt_users.sort(key=lambda x: x['followers_count'], reverse=True)
        rt_user_images = [x['profile_image_url'].replace('_normal', '') for x in rt_users]
        h.tweet_data = json.dumps(rt_user_images)
        h.last_updated = datetime.now()
        h.etag = hashlib.sha1(json.dumps(rt_user_images)).hexdigest()
    db.session.commit()


def init():
    handles = ['github', 'timoreilly', 'twitter', 'martinfowler', 'gvanrossum', 'BillGates', 'spolsky', 'firefox', 'dhh']
    for h in handles:
        u = User(screen_name=h)
        db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    update()