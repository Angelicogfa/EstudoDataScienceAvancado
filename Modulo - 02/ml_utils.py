import re
import os
import time
import json
import numpy as np
import pandas as pd
import joblib as jb
from lightgbm import LGBMClassifier
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import LogisticRegression


mapa_meses = {
    'jan': 'Jan',
    'fev': 'Feb',
    'mar': 'Mar',
    'abr': 'Apr',
    'mai': 'May',
    'jun': 'Jun',
    'jul': 'Jul',
    'ago': 'Aug',
    'set': 'Sep',
    'out': 'Oct',
    'nov': 'Nov',
    'dez': 'Dec'
}

regex = re.compile(r'(\d+) de (\w+)\. de (\d+)')

path_site = os.path.realpath(os.path.dirname(__file__))

mdl_lr: LogisticRegression = jb.load(os.path.join(path_site, 'logistic_regression_20210406.pkl.z'))
mdl_lgbm: LGBMClassifier = jb.load(os.path.join(path_site, 'lgbm_20210406.pkl.z'))
vectorize = jb.load(os.path.join(path_site, 'title_vectorize_20210406.pkl.z'))

def compute_prediction(data: dict) -> float:
    feature_array = __compute_feature(data)

    if feature_array is None:
       return 0

    p_lr = mdl_lr.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]

    p = 0.2 * p_lr + 0.8 * p_lgbm
    ## __log_data(data, feature_array, p)
    return p

def __log_data(data: dict, feature: csr_matrix, p: float):
    video_id = data['link']
    data['prediction'] = p
    data['feature_array'] = feature.todense().tolist()
    print(video_id, json.dumps(data))


def __clean_date(data: dict):
    if regex.match(data['video_date']) is None:
        return None

    date = list(regex.match(data['video_date']).groups())

    if len(date[0]) == 1:
        date[0] = '0' + date[0]
    
    date[1] = mapa_meses[date[1]]

    clear_date = " ".join(date)
    return pd.to_datetime(clear_date, format='%d %b %Y')

def __compute_feature(data: dict):

    publish_date = __clean_date(data)
    if publish_date is None:
        return None

    views = data['view_counts']
    title = data.get('title')

    if title is None:
        return None

    features = dict()
    features['tempo_desde_pub'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features['views'] = views
    features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
    del features['tempo_desde_pub']

    vectorize_title = vectorize.transform([title])
    num_features = csr_matrix(np.array([features['views'], features['views_por_dia']]))
    feature_array = hstack([num_features, vectorize_title])

    return feature_array