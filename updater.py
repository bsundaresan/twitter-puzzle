__author__ = 'ishaan'

from multunus_twitter_challenge.models import User
from multunus_twitter_challenge import twitter_api
from multunus_twitter_challenge import db
import json
from datetime import datetime
import hashlib


handles = ['github', 'timoreilly', 'twitter', 'martinfowler', 'gvanrossum', 'BillGates', 'spolsky', 'firefox', 'dhh']


def get_profile_image(screen_name):
    """
    Gets profile image for the given handle
    """
    user_info = twitter_api.get_user_info(screen_name=screen_name)
    if not user_info:
        return
    image_url = user_info.get('profile_image_url')
    image_url = image_url.replace('_normal', '')
    return image_url


def update():
    """
    Updates the rankings for all handles
    """
    all_handles = User.query.all()
    if not all_handles:
        print "User objects not found.....Creating..\n\n"
        init()
        all_handles = User.query.all()

    for h in all_handles:
        print h.screen_name + '\n'
        tweet_id = h.tweet_id
        if not tweet_id:
            print "Existing Tweet not found...Trying to get one\n"
            if not change_tweet(h):
                print "Could not Update " + h.screen_name + '\n'
                continue
            tweet_id = h.tweet_id
        rt_ids = twitter_api.get_retweeters(tweet_id)
        if not rt_ids:
            print "Could not Update " + h.screen_name + '\n'
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


def change_tweet(user):
    """
    Selects a new tweet to calculate ranks for the specified user object
    """
    tweet = twitter_api.get_tweet(user.screen_name)
    if tweet:
        user.tweet_id = tweet['id_str']
        user.tweet_text = tweet['text']
        db.session.commit()
        return True
    else:
        return False


def init():
    """
    Creates DB entry for all 9 handles and gets their profile image
    """
    for h in handles:
        u = User(screen_name=h)
        db.session.add(u)
        u.profile_image_url = get_profile_image(h)
    db.session.commit()

if __name__ == '__main__':
    update()