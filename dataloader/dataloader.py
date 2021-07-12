# -*- coding: utf-8 -*-
"""Data Loader"""
from utils.my_utils import load_data

class DataLoader:
    """Data Loader class"""

    @staticmethod
    def load_data(data_config):
        """Loads dataset from path"""
        session_df_normalized, session_df, requests_df = \
            load_data(log_path=data_config.path, req_thres=data_config.req_threshold, normalize_feat=True)

        return session_df_normalized