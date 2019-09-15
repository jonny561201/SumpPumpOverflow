import json
from datetime import datetime

import requests

POST_SUMP_CURRENT = 'http://localhost:8080/sumpPump/user/{}/currentDepth'


def save_current_daily_depth(user_id, depth, time):
    url = POST_SUMP_CURRENT.format(user_id)
    date = datetime.fromtimestamp(time)
    post_body = {'depth': depth, 'datetime': str(date)}

    requests.post(url, data=json.dumps(post_body))
