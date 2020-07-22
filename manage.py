import threading
import tweet
from TweetListener import TweetListener
from dotenv import load_dotenv
load_dotenv()

# tweet.init()

tweetListener = TweetListener()

tweets = tweetListener.get_tweets()

data = [tweet['text'] for tweet in tweets]

print(data)