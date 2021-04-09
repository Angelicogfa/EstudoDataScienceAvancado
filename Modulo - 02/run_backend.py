from get_data import *
from ml_utils import *
from multiprocessing import Pool
import os
import json
import time

queries = ['machine+learning', 'data+science', 'kaggle']

def __processing_page(page) -> dict:
    video_json_data = download_video_page(page['link'])

    p = compute_prediction(video_json_data)

    video_id = video_json_data.get('link', '')
    data_front = dict(title=video_json_data.get('title', ''),
    score=float(p), video_id=video_id)
    data_front['update_time'] = time.time_ns()
    return data_front

def update_db(logging=True):
    path_site = os.path.realpath(os.path.dirname(__file__))

    jsons = []
    agents = 4
    chunksize = 3
    for query in queries:
        video_list = download_search_page(query)
        
        with Pool(processes=agents) as pool:
            result = pool.map(__processing_page, video_list, chunksize=chunksize)
            jsons += result

    with open(os.path.join(path_site, 'novos_videos.json'), 'w+', encoding='utf-8') as output:
        output.write(json.dumps(jsons))
                
    return True