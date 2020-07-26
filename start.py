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
        out += word + " "

    return out.strip()


def to_predict(tweets):
    l = []
    for tweet in tweets:
        if(tweet["id"] not in predicted):
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

    print("predicting")

    if(len(data["list"]) == 0):
        predicted = []
        return

    tweets = to_predict(data["list"])

    predict_list = [str(tweet['text']) for tweet in tweets]

    if(len(predict_list) > 0):
        predictions = model.predict(predict_list)
        print(predictions)

        i = 0
        for prediction in predictions:
            if(prediction == "pos"):
                requests.get(APP_URL + '/tweet/' +
                             str(tweets[i]['id']) + '/approve/')
            elif(prediction == "neg"):
                requests.get(APP_URL + '/tweet/' +
                             str(tweets[i]['id']) + '/reject/')

            predicted.append(tweets[i]['id'])

            i += 1


sio.connect(APP_URL)