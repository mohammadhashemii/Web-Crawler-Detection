# -*- coding: utf-8 -*-
""" main.py """

from configs.config import CFG
from models.Autoencoder import Autoencoder


def run():

    model = Autoencoder(CFG)
    print(">> LOADING THE DATA...")
    model.load_data()
    print(">> BUILDING THE MODEL...")
    model.build()
    print(">> PREDICTING...")
    model.predict()


if __name__ == '__main__':
    run()