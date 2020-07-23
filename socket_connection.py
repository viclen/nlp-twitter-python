import socketio
import requests
import predictor


predicted = []
model = predictor.create()
APP_URL = 'https://twitter-watcher-backend.herokuapp.com'

sio = socketio.Client()


def remove_hashtags(text):
    out = ""
    words = str(text).split(' ')
    for word in words:
        if("#" not in word and "@" not in word):
            out += word + " "

    return out.strip()


def to_predict(tweets):
    l = []
    for tweet in tweets:
        if(tweet["id"] not in predicted):
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
    print("predicting")

    tweets = to_predict(data["list"])

    data = [tweet['text'] for tweet in tweets]
    predictions = model.predict(data)

    print(predictions)

    i = 0
    for prediction in predictions:
        if(prediction == "pos"):
            requests.get(APP_URL + '/tweet/' + tweets[i]['id'] + '/approve/')
        else:
            requests.get(APP_URL + '/tweet/' + tweets[i]['id'] + '/reject/')

        predicted.append(tweets[i]['id'])

        i += 1


sio.connect(APP_URL)
