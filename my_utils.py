import numpy as np
import pandas as pd
import re
import json
import warnings
from user_agents import parse
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler

def use_api(raw_user_agent, api_key):
    
    # You can get your API Key by following these instructions:
    # https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#introduction-api-key

    
    # Where will the request be sent to
    api_url = "https://api.whatismybrowser.com/api/v2/user_agent_parse"
    
    # -- Set up HTTP Headers
    headers = {
        'X-API-KEY': api_key,
    }
    
    # -- prepare data for the API request
    # This shows the `parse_options` key with some options you can choose to enable if you want
    # https://developers.whatismybrowser.com/api/docs/v2/integration-guide/#user-agent-parse-parse-options
    post_data = {
        'user_agent': raw_user_agent,
        "parse_options": {
        }
    }
    
    # -- Make the request
    result = requests.post(api_url, data=json.dumps(post_data), headers=headers)
    
    # -- Try to decode the api response as json
    result_json = {}
    try:
        result_json = result.json()
    except Exception as e:
        print(result.text)
        print("Couldn't decode the response as JSON:", e)
        exit()
        
    parse = result_json.get('parse')
    
    return parse.get('simple_software_string')


def create_user_agents_dic(user_agents_set, api_key, json_path="user_agent.json"):
    user_agents_dic = {} 
    idx = 0

    print("Start to create the json file ...")
    for ua in user_agents_set:
        if idx % 500 == 0:
            print("{} user agents have been saved!".format(idx))

        api_result = use_api(ua, api_key)
        user_agents_dic[ua] = api_result
        idx = idx + 1

    with open(json_path, 'w') as fp:
        json.dump(user_agents_dic, fp)


def create_DataFrame(csv_path='output.log'):
    regex = r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])'    
    
    df = pd.read_csv(csv_path, 
          sep=regex, 
          engine='python',  
          names=['ip', 'time', 'request', 'status_code', 'response_length', 'user_agent', 'response_time'],           
          na_values='-', header=None, error_bad_lines=False)
    
    df.time = df.time.apply(lambda x : x.strip("[|]"))
    df.request = df.request.apply(lambda x : x.strip("[|]"))
    df.user_agent = df.user_agent.apply(lambda x : x.strip("[|]"))
    
    df["method"] = df.request.apply(lambda x : x.split(" ")[0])
    df.request = df.request.apply(lambda x : x.split(" ")[1])
    df.rename(columns={"request" : "path"}, inplace=True)
    
    df.time = pd.to_datetime(df.time, unit='ns')
    df = df.reindex(columns=['ip', 'time', 'method', 'status_code','path', 'response_length', 'user_agent', 'response_time'])
    df.path = df.path.apply(lambda x : x.strip("/"))
    
    return df


def load_data(csv_path='output.log', req_thres=5, normalize_feat=True):

    print("LOADING THE DATASET...")
 
    # load the csv file into a DataFrame
    df = create_DataFrame(csv_path=csv_path)
    # drop all the records with ip = NaN values
    df.drop(df[df['ip'].isna()].index, inplace = True)
    # fill the NaN values with 0 for response_time column
    df['response_time'] = df['response_time'].fillna(0)
    # add a column into the main dataframe which indicates the normalized count of the path for each request.
    # note that "len" counts the NaN value as well.
    df['path_count_normalized'] = df.groupby(['path'])['path'].transform(len)
    df['path_count_normalized'] = (df['path_count_normalized'] / len(df)) * 100


    # --------- Features per each session ---------

    # ------ 1. number of requests per user
    user_df = pd.DataFrame(df.groupby(['ip', 'user_agent']).size(), columns=['requests_count'])
    user_df.sort_values('requests_count', ascending=False)

    # ------ 2. STD of path length per user
    df['path_length'] = df['path'].apply(lambda x : len(x.split('/')))
    user_df['path_length_std'] = df.groupby(['ip', 'user_agent'])['path_length'].agg('std')
    user_df['path_length_std'] = user_df['path_length_std'].fillna(0)

    # ------ 3. Percentage of 4xx response codes per session
    resp_400 = df[df['status_code'] > 400]
    user_df['4xx_counts'] = resp_400.groupby(['ip', 'user_agent'])['status_code'].agg('size')
    user_df['4xx_counts'] = user_df['4xx_counts'].fillna(0)
    user_df['4xx_percentage(%)'] = (user_df['4xx_counts'] / user_df['requests_count']) * 100
    user_df.drop(columns=['4xx_counts'], inplace=True)

    # ------ 4. Percentage of 3xx response codes per session
    resp_300 = df[(df['status_code'] >= 300) & (df['status_code'] < 400)]
    user_df['3xx_counts'] = resp_300.groupby(['ip', 'user_agent'])['status_code'].agg('size')
    user_df['3xx_counts'] = user_df['3xx_counts'].fillna(0)
    user_df['3xx_percentage(%)'] = (user_df['3xx_counts'] / user_df['requests_count']) * 100
    user_df.drop(columns=['3xx_counts'], inplace=True)

    # ------ 5. Percentage of HTTP HEAD requests, per session
    HTTP_HEAD = df[df['method'] == 'Head']
    user_df['HEAD_count'] = HTTP_HEAD.groupby(['ip', 'user_agent'])['method'].agg('size')
    user_df['HEAD_count'] = user_df['HEAD_count'].fillna(0)
    user_df['HEAD_count(%)'] = (user_df['HEAD_count'] / user_df['requests_count']) * 100
    user_df.drop(columns=['HEAD_count'], inplace=True)

    # ------ 6. Percentage of image requests per session
    image_requests = df[df['path'].str.contains('images',case=False)]
    user_df['image_count'] = image_requests.groupby(['ip', 'user_agent'])['path'].agg('size')
    user_df['image_count'] = user_df['image_count'].fillna(0)
    user_df['image_count(%)'] = (user_df['image_count'] / user_df['requests_count']) * 100
    user_df.drop(columns=['image_count'], inplace=True)

    # ------ 7. Average and sum of the response length and response time per session
    user_df['total_response_length'] = df.groupby(['ip', 'user_agent'])['response_length'].agg('sum')
    user_df['mean_response_length'] = df.groupby(['ip', 'user_agent'])['response_length'].agg('mean')
    user_df['total_response_time'] = df.groupby(['ip', 'user_agent'])['response_time'].agg('sum')
    user_df['mean_response_time'] = df.groupby(['ip', 'user_agent'])['response_time'].agg('mean')

    # ------ 8. Average of the path_count_normalized per user
    user_df['avg_path_count_norm'] = df.groupby(['ip', 'user_agent'])['path_count_normalized'].agg('mean')

    # ------ 9. Set the browser for each user agent
    user_df = user_df.reset_index()
    user_df['browser'] = user_df['user_agent'].apply(lambda x: parse(x).browser.family)
    user_df['os'] = user_df['user_agent'].apply(lambda x: parse(x).os.family)
    user_df['is_bot'] = user_df['user_agent'].apply(lambda x: parse(x).is_bot)
    user_df['is_pc'] = user_df['user_agent'].apply(lambda x: parse(x).is_pc)

    # ------ 10. Average of time between requests per session

    # first we drop all the sessions with less than req_thres requests
    user_df.drop(user_df[user_df["requests_count"] < req_thres].index, inplace=True)
    user_df.set_index(['ip', 'user_agent'], inplace=True)
    df['time_stamp'] = df['time'].values.astype(np.int64) // 10 ** 9
    user_df['avg_time_diff'] = df.groupby(['ip', 'user_agent'])['time_stamp'].agg(lambda group: group.sort_values().sum())
    user_df['avg_time_diff'] = user_df['avg_time_diff'] / (user_df['requests_count'] - 1)

    X = user_df.copy()

    if normalize_feat:
        

        # normalize columns
        to_be_normalized = ['requests_count',
                            'total_response_length',
                            '3xx_percentage(%)',
                            '4xx_percentage(%)',
                            'HEAD_count(%)',
                            'image_count(%)',
                            'mean_response_length',
                            'total_response_time',
                            'mean_response_time',
                            'avg_time_diff']

        scaler = StandardScaler()
        X[to_be_normalized] = scaler.fit_transform(X[to_be_normalized])


        # Get one hot encoding of some columns
        to_be_oh_encoded = ['browser', 'os']
        oh = pd.get_dummies(X[to_be_oh_encoded], drop_first=True)
        # Join the encoded df
        X = X.join(oh)
        X.drop(['browser', 'os'], axis=1, inplace=True)

    print("DATASET HAS BEEN LOADED SUCESSFULLY!")

    return X, user_df, df




 
