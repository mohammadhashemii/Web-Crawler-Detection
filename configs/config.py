# -*- coding: utf-8 -*-
"""configs in json format"""

import json

CFG = {
    "data": {
        "path": "/Users/mohammad/Documents/git/Web-Crawler-Detection/dataset/output.log",
        "req_threshold": 4,
        "features": ['requests_count', 'path_length_std', '4xx_percentage(%)',
                    '3xx_percentage(%)', 'HEAD_count(%)', 'image_count(%)',
                    'total_response_length', 'mean_response_length', 'total_response_time',
                    'mean_response_time', 'avg_path_count_norm', 'robots_txt_reqs',
                    'is_bot', 'is_pc', 'avg_time_diff']
    },
    "train": {
        "batch_size": 64,
        "epochs": 25,
        "loss": 'mean_squared_error',
        "optimizer": "adam",
        "metric": "accuracy"
    },
    "predict": {
        "model_weights": "/Users/mohammad/Documents/git/Web-Crawler-Detection/checkpoints/autoencoder_weights_01.h5",
        "mse_threshold": 0.688
    }
}


class Config:
    """Config class which contains data, train and model hyperparameters"""

    def __init__(self, data, train, predict):
        self.data = data
        self.train = train
        self.predict = predict

    @classmethod
    def from_json(cls, cfg):
        """Creates config from json"""
        params = json.loads(json.dumps(cfg), object_hook=HelperObject)
        return cls(params.data, params.train, params.predict)


class HelperObject(object):
    """Helper class to convert json into Python object"""
    def __init__(self, dict_):
        self.__dict__.update(dict_)