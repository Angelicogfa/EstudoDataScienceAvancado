from get_data import *
from ml_utils import *
import os
import json
import time

queries = ['machine+learning', 'data+science', 'kaggle']

def update_db():
    path_site = os.path.realpath(os.path.dirname(__file__))

    jsons = []
    for query in queries:
        video_list = download_search_page(query)
        
        for video in video_list:
            video_json_data = download_video_page(video['link'])

            p = compute_prediction(video_json_data)

            video_id = video_json_data.get('link', '')
            data_front = dict(title=video_json_data.get('title', ''),
            score=float(p), video_id=video_id)
            data_front['update_time'] = time.time_ns()

            print(video_id, json.dumps(data_front))
            jsons.append(data_front)

    with open(os.path.join(path_site, 'novos_videos.json'), 'w+', encoding='utf-8') as output:
        output.write(json.dumps(jsons))
                
    return True