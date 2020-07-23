import socketio
import predictor

model = predictor.create()


def remove_hashtags(text):
    out = ""
    words = str(text).split(' ')
    for word in words:
        if("#" not in word and "@" not in word):
            out += word + " "

    return out.strip()


# standard Python
sio = socketio.Client()


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
    tweets = data["list"]
    data = [remove_hashtags(tweet['text']) for tweet in tweets]
    predictions = model.predict(data)

    for prediction in predictions:
        print(prediction)


sio.connect('https://twitter-watcher-backend.herokuapp.com/')
