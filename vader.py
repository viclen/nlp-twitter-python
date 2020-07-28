from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from os import system, name as so_name
import requests
import logging

# remove log from socket io
logging.basicConfig(filename=os.devnull, filemode='w')
if(True):
    import socketio

APP_URL = 'https://twitter-watcher-backend.herokuapp.com'

# socket io
sio = socketio.Client(logger=False, engineio_logger=False)

# create predictor
predicted = []

predictor = SentimentIntensityAnalyzer()


def remove_hashtags(text):
    out = ""
    words = str(text).split(' ')
    for word in words:
        if("@" not in word and "https://" not in word and not ("&" in word and ";" in word)):
            out += word.replace('#', '') + " "

    return out.strip()


def to_predict(tweets):
    l = []
    for tweet in tweets:
        if(tweet['id'] not in predicted):
            predicted.append(tweet['id'])
            l.append({
                'id': tweet['id'],
                'text': tweet['text']
            })

    return l


@sio.event
def connect():
    print("Connected!\n")


@sio.event
def connect_error():
    pass


@sio.event
def disconnect():
    print("Disconnected")


@sio.event
def change(data):
    global predicted

    if(len(data["list"]) == 0):
        predicted = []
        return

    tweets = to_predict(data["list"])

    if(len(tweets)):
        print('Predicting')

    for tweet in tweets:
        score = predictor.polarity_scores(remove_hashtags(tweet['text']))

        print(score)

        # score['pos'] > score['neg'] and score['pos'] > score['neu']:
        if score['compound'] >= 0:
            # positive
            requests.get(APP_URL + '/tweet/' +
                         str(tweet['id']) + '/approve/')
        else:  # elif score['neg'] > score['neu']:
            # negative
            requests.get(APP_URL + '/tweet/' +
                         str(tweet['id']) + '/reject/')
        # else:
        #     # neutral
        #     print('neutral: {}'.format(tweet['text']))


sio.connect(APP_URL)
