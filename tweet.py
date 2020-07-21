import os
import tweepy
from TweetListener import TweetListener


def init():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'),
                               os.getenv('TWITTER_API_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                          os.getenv('TWITTER_ACCESS_SECRET'))

    tweetListener = TweetListener()
    tweetStream = tweepy.Stream(auth=auth, listener=tweetListener)
    tweetStream.filter(track=['covid19'])
