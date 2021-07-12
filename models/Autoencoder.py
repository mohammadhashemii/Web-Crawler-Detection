# -*- coding: utf-8 -*-
"""Autoencoder model"""

#internal
from dataloader.dataloader import DataLoader
from configs.config import Config

class Autoencoder():
    """Autoencoder Model Class"""

    def __init__(self, config):
        self.dataset = None
        self.config = Config.from_json(config)

    def load_data(self):
        """Loads data """
        self.dataset = DataLoader().load_data(self.config.data)
        print(self.dataset.shape)