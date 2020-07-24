import numpy as np
import pandas as pd
import tensorflow as tf
import ktrain
from ktrain import text
from TweetListener import TweetListener
from sklearn.model_selection import train_test_split

def create():
    print("Preparing dataset")
    dataset = pd.read_csv("./drive/My Drive/NLP/imdb-reviews-pt-br.csv")
    X = dataset.drop('text_en', axis=1).rename(columns={"text_pt": "text"})
    y = dataset.sentiment
    data_train, data_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # dataset = pd.read_csv("./drive/My Drive/NLP/ktrain/Train3Classes.csv", ";")
    # dataset.sentiment = dataset.sentiment.replace([0, 2, 1], ['neg', 'neu', 'pos'])
    # data_train = dataset.drop(labels=['id', 'query_used', 'tweet_date'], axis=1).rename(columns={ "tweet_text": "text" })

    # dataset = pd.read_csv("./drive/My Drive/NLP/ktrain/Test3Classes.csv", ";")
    # dataset.sentiment = dataset.sentiment.replace([0, 2, 1], ['neg', 'neu', 'pos'])
    # data_test = dataset.drop(labels=['id', 'query_used', 'tweet_date'], axis=1).rename(columns={ "tweet_text": "text" })

    (X_train, y_train), (X_test, y_test), preprocess = text.texts_from_df(
        train_df=data_train,
        text_column='text',
        label_columns='sentiment',
        val_df=data_test,
        maxlen=400,
        preprocess_mode='bert',
        verbose=0,
        lang='pt'
    )

    print("Creating model")
    model = text.text_classifier(
        name='bert',
        train_data=(X_train, y_train),
        preproc=preprocess,
        verbose=0
    )

    print("Creating learner")
    learner = ktrain.get_learner(
        model=model,
        train_data=(X_train, y_train),
        val_data=(X_test, y_test),
        batch_size=6
    )

    print("Loading saved model")
    learner.load_model('./drive/My Drive/NLP/ktrain/model')

    print("Creating predictor")
    return ktrain.get_predictor(learner.model, preprocess)
