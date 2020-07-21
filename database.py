import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os


def init():
    cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    firebase_admin.initialize_app(cred, {
        'databaseUrl': "https://twitter-sentiment-python.firebaseio.com"
    })
    return firestore.client()
