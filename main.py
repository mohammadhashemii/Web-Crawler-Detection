# -*- coding: utf-8 -*-
""" main.py """

from configs.config import CFG
from models.Autoencoder import Autoencoder


def run():

    model = Autoencoder(CFG)
    model.load_data()
    #model.build()
    #model.predict()


if __name__ == '__main__':
    run()