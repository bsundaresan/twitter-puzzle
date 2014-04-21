__author__ = 'ishaan'

from models import User
import twitter_api
from multunus_twitter_challenge import db
import json


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


def update():
    handles = User.query.all()
    for h in handles:
        rt_ids = twitter_api.get_retweeters(h.tweet_id)
        if not rt_ids:
            continue
        rt_users = []
        for user_id in rt_ids['ids'][:10]:
            user_info = twitter_api.get_user_info(user_id=user_id)
            if user_info:
                rt_users.append(user_info)
        rt_users.sort(key=lambda x: x['followers_count'], reverse=True)
        rt_user_images = [x['profile_image_url'].replace('_normal', '') for x in rt_users]
        h.tweet_data = json.dumps(rt_user_images)
    db.session.commit()