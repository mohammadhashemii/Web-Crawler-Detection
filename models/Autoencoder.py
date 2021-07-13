# -*- coding: utf-8 -*-
"""Autoencoder model"""

#internal
from dataloader.dataloader import DataLoader
from configs.config import Config

#external
from keras.models import Model, load_model
from keras.layers import Input, Dense


class Autoencoder():
    """Autoencoder Model Class"""

    def __init__(self, config):
        self.data = None
        self.config = Config.from_json(config)

        self.model = None
        self.epochs = self.config.train.epochs
        self.batch_size = self.config.train.batch_size
        self.loss = self.config.train.loss
        self.optimizer = self.config.train.optimizer
        self.metric = self.config.train.metric

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
        hidden_dim = int(encoding_dim / 2)  # hidden layer

        # model architecture
        input_layer = Input(shape=(input_dim))
        encoder = Dense(encoding_dim, activation="relu")(input_layer)
        encoder = Dense(hidden_dim, activation="relu")(encoder)
        decoder = Dense(encoding_dim, activation='relu')(encoder)
        decoder = Dense(input_dim, activation='relu')(decoder)
        self.model = Model(inputs=input_layer, outputs=decoder)

        # compile the model
        self.model.compile(optimizer=self.optimizer,
                            loss=self.loss,
                            metrics=self.metric)

        # model summary
        print(self.model.summary())
        with open('./models/autoencoder_architecture.txt', 'w') as f:
            self.model.summary(print_fn=lambda x: f.write(x + '\n'))



