__author__ = 'ishaan'

import config
import requests
import json
from requests_oauthlib import OAuth1

oauth = OAuth1(config.APP_KEY, client_secret=config.APP_SECRET, resource_owner_key=config.ACCESS_TOKEN,
               resource_owner_secret=config.ACCESS_TOKEN_SECRET
               )


def get_tweets(screen_name, count=15):
    """
    Returns count number of tweets for the specified user
    """
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name': screen_name,
              'count': count
              }
    try:
        r = requests.get(url, params=params, auth=oauth)
        return json.loads(r.text)
    except Exception as e:
        print e
        return False


def get_user_info(**kwargs):
    """
    Returns user info for the specified user
    Kwargs - screen_name, user_id
    Either of screen_name or user_id must be passed
    """
    url = 'https://api.twitter.com/1.1/users/show.json'
    screen_name = kwargs.get('screen_name')
    user_id = kwargs.get('user_id')
    params = {'screen_name': screen_name,
              'user_id': user_id,
              'include_entities': 'false'
              }
    try:
        r = requests.get(url, params=params, auth=oauth)
        return json.loads(r.text)
    except Exception as e:
        print e
        return False


def get_retweeters(tweet_id, cursor=-1):
    """
    Returns list of user ids who have retweeted the specified tweet
    """
    url = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
    params = {'id': tweet_id,
              'cursor': cursor,
              'stringify_ids': 'true'
              }
    try:
        r = requests.get(url, params=params, auth=oauth)
        return json.loads(r.text)
    except Exception as e:
        print e
        return False