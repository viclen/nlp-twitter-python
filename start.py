import os
from os import system, name as so_name
import requests
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import threading

# remove log from socket io
logging.basicConfig(filename=os.devnull, filemode='w')
if(True):
    import socketio
    import predictor

APP_URL = 'https://twitter-watcher-backend.herokuapp.com'

# socket io
sio = socketio.Client(logger=False, engineio_logger=False)

# create predictor
predicted = []
model = predictor.create()
vader = SentimentIntensityAnalyzer()
requests_to_make = []


def log(text):
    file = open('log.txt', 'a')
    file.write(text)
    file.close()


def remove_hashtags(text):
    out = ""
    words = str(text).split(' ')
    for word in words:
        # and not ("&" in word and ";" in word):
        if "@" not in word and "https://" not in word:
            out += word.replace('#', '') + " "

    return out.strip()


def to_predict(tweets):
    l = []
    for tweet in tweets:
        if(tweet['id'] not in predicted):
            predicted.append(tweet['id'])
            l.append({
                'id': tweet['id'],
                'text': remove_hashtags(tweet['text'])
            })

    return l


def make_requests():
    threading.Timer(1.0, make_requests).start()

    # os.system('clear')
    # print('requests: {}'.format(requests_to_make))

    if(len(requests_to_make) > 0):
        requests.get(requests_to_make.pop(0))


@sio.event
def connect():
    log("Connected!\n")


@sio.event
def connect_error(err):
    log(err)
    pass


@sio.event
def disconnect():
    log("Disconnected")


@sio.event
def change(data):
    global predicted

    if(len(data["list"]) == 0):
        predicted = []
        return

    tweets = to_predict(data["list"])

    predict_list = [tweet['text'] for tweet in tweets]

    if(len(predict_list) > 0):
        print("predicting")

        scores = []
        for text in predict_list:
            score = vader.polarity_scores(text)

            # score['pos'] > score['neg'] and score['pos'] > score['neu']:
            if score['compound'] >= 0.05:
                # positive
                scores.append('pos')
            elif score['compound'] <= -0.05:
                # negative
                scores.append('neg')
            else:
                scores.append('neu')

        predictions = model.predict(predict_list)

        i = 0
        for prediction in predictions:
            log("{}, {}:  {}".format(
                prediction, scores[i], tweets[i]['text']))

            if prediction == "pos" and scores[i] != "neg":
                requests_to_make.append(APP_URL + '/tweet/' +
                                        str(tweets[i]['id']) + '/approve/')
            else:
                requests_to_make.append(APP_URL + '/tweet/' +
                                        str(tweets[i]['id']) + '/reject/')

            i += 1


make_requests()
sio.connect(APP_URL)
