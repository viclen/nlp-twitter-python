import os
from os import system, name as so_name
import requests
import logging

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
                'text': remove_hashtags(tweet['text'])
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

    predict_list = [tweet['text'] for tweet in tweets]

    if(len(predict_list) > 0):
        print("predicting")

        predictions = model.predict(predict_list)

        i = 0
        for prediction in predictions:
            print("{}:  {}".format(prediction, tweets[i]['text']))

            if(prediction == "pos"):
                requests.get(APP_URL + '/tweet/' +
                             str(tweets[i]['id']) + '/approve/')
            elif(prediction == "neg"):
                requests.get(APP_URL + '/tweet/' +
                             str(tweets[i]['id']) + '/reject/')

            i += 1


sio.connect(APP_URL)
