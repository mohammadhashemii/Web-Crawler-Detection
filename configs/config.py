# -*- coding: utf-8 -*-
"""configs in json format"""

import json

CFG = {
    "data": {
        "path": "./dataset/output.log",
        "req_threshold": 4,
    },
    "train": {
        "batch_size": 64,
        "epoches": 25,
        "loss": 'mean_squared_error',
        "optimizer": {
            "type": "adam"
        },
        "metrics": ["accuracy"]
    }
}


class Config:
    """Config class which contains data, train and model hyperparameters"""

    def __init__(self, data, train):
        self.data = data
        self.train = train

    @classmethod
    def from_json(cls, cfg):
        """Creates config from json"""
        params = json.loads(json.dumps(cfg), object_hook=HelperObject)
        return cls(params.data, params.train)


class HelperObject(object):
    """Helper class to convert json into Python object"""
    def __init__(self, dict_):
        self.__dict__.update(dict_)