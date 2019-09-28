import json
import logging
from datetime import datetime, date

import requests

POST_SUMP_CURRENT = 'http://localhost:8080/sumpPump/user/{}/currentDepth'
POST_SUMP_AVERAGE = 'http://localhost:8080/sumpPump/user/{}/averageDepth'
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


def save_current_depth(user_id, depth, time):
    url = POST_SUMP_CURRENT.format(user_id)
    current_time = datetime.fromtimestamp(time)
    post_body = {'depth': depth, 'datetime': str(current_time)}

    response = requests.post(url, data=json.dumps(post_body), headers=DEFAULT_HEADERS)
    logging.info('Saved current depth response: ' + response.status_code)

    return response


def save_daily_average_depth(user_id, depth):
    url = POST_SUMP_AVERAGE.format(user_id)
    current_date = date.today()
    post_body = {'depth': depth, 'date': str(current_date)}

    response = requests.post(url, data=json.dumps(post_body), headers=DEFAULT_HEADERS)
    logging.info('Saved daily average depth response: ' + response.status_code)

    return response


def send_alert():
    pass


def send_warning():
    pass
