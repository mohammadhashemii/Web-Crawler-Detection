# -*- coding: utf-8 -*-
"""Autoencoder model"""

#internal
from dataloader.dataloader import DataLoader
from configs.config import Config

#external
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense


class Autoencoder():
    """Autoencoder Model Class"""

    def __init__(self, config):
        # load data
        self.data = None
        self.config = Config.from_json(config)

        # build
        self.model = None
        self.epochs = self.config.train.epochs
        self.batch_size = self.config.train.batch_size
        self.loss = self.config.train.loss
        self.optimizer = self.config.train.optimizer
        self.metric = self.config.train.metric

        # predict
        self.model_weights = self.config.predict.model_weights
        self.mse_threshold = self.config.predict.mse_threshold
        self.results = None

    def load_data(self):
        """Loads data"""

        self.data = DataLoader().load_data(self.config.data)
        # set the features which the model will use
        self.data = self.data[self.config.data.features]
        print("- features which the model will use:")
        print(self.data.columns)

    def build(self):
        """build and compile the keras model"""
        input_dim = self.data.shape[1]  # the # features
        encoding_dim = input_dim  # first layer
        hidden_dim1 = int(encoding_dim / 2)  # hidden layer 1
        hidden_dim2 = int(encoding_dim / 4)  # hidden layer 1

        # model architecture
        input_layer = Input(shape=(input_dim))
        encoder = Dense(encoding_dim, activation="relu")(input_layer)
        encoder = Dense(hidden_dim2, activation="relu")(encoder)
        decoder = Dense(encoding_dim, activation="relu")(encoder)
        decoder = Dense(input_dim, activation='relu')(decoder)
        self.model = Model(inputs=input_layer, outputs=decoder)

        # compile the model
        self.model.compile(optimizer=self.optimizer,
                            loss=self.loss,
                            metrics=self.metric)

        # model summary
        self.model.summary()
        #with open('./models/autoencoder_architecture.txt', 'w') as f:
        #    self.model.summary(print_fn=lambda x: f.write(x + '\n'))

    def predict(self):
        """predict some observation"""
        self.model.load_weights(self.model_weights)

        preds = self.model.predict(self.data)
        # get the error term
        mse = np.mean(np.power(self.data.to_numpy() - preds, 2), axis=1)

        self.data['mse'] = mse
        self.data['is_crawler'] = mse > self.mse_threshold
        self.data['is_crawler'] = self.data['is_crawler'].astype(int)

        self.results = self.data.reset_index()
        self.results = self.results[['ip', 'user_agent', 'mse', 'is_crawler']]
        self.results = self.results.round(3)
        print(self.results.to_string())

        return self.results








