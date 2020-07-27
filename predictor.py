import numpy as np
import pandas as pd
import tensorflow as tf
import ktrain
from ktrain import text
from TweetListener import TweetListener
from sklearn.model_selection import train_test_split


def create():
    print("Preparing dataset")

    dataset = pd.read_csv("./drive/My Drive/NLP/EN/dataset.csv",
                          ",", encoding='ISO-8859-1')
    dataset.columns = ['id', 'sentiment', 'text']
    dataset = dataset.drop(labels=['id'], axis=1)

    dataset.sentiment = dataset.sentiment.replace(
        [0, 0.5, 1], ['neg', 'neu', 'pos'])

    data_train = dataset[(dataset.index > np.percentile(dataset.index, 0)) & (
        dataset.index <= np.percentile(dataset.index, 50))]
    data_test = dataset[(dataset.index > np.percentile(dataset.index, 81)) & (
        dataset.index <= np.percentile(dataset.index, 100))]

    (X_train, y_train), (X_test, y_test), preprocess = text.texts_from_df(
        train_df=data_train,
        text_column='text',
        label_columns='sentiment',
        val_df=data_test,
        maxlen=400,
        preprocess_mode='bert',
        verbose=0,
        lang='en'
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
    learner.load_model('./drive/My Drive/NLP/EN/model')

    print("Creating predictor")
    return ktrain.get_predictor(learner.model, preprocess)