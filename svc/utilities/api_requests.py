import json
from datetime import datetime

import requests


def save_current_daily_depth(user_id, depth, time):
    url = 'http://localhost:8080/sumpPump/user/' + user_id + '/currentDepth'
    date = datetime.fromtimestamp(time)
    post_body = {'depth': depth, 'datetime': str(date)}

    requests.post(url, data=json.dumps(post_body))
