# -*- coding: utf-8 -*-
"""configs in json format"""

CFG = {
    "data": {
        "path": "../dataset/output.log",
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