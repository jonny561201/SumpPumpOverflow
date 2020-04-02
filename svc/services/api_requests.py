import json
import logging
from datetime import datetime, date

import requests

from svc.utilities.url import get_hub_base_url

POST_SUMP_CURRENT_URL = '{}/sumpPump/user/{}/currentDepth'
POST_SUMP_AVERAGE_URL = '{}/sumpPump/user/{}/averageDepth'
DEFAULT_HEADERS = {'Content-Type': 'text/json'}


def save_current_depth(user_id, depth, time, alert_level):
    base_url = get_hub_base_url()
    url = POST_SUMP_CURRENT_URL.format(base_url, user_id)
    current_time = datetime.fromtimestamp(time)
    post_body = {'depth': depth, 'alert_level': alert_level, 'datetime': str(current_time)}

    response = requests.post(url, data=json.dumps(post_body), headers=DEFAULT_HEADERS)
    logging.info('Saved current depth response: {}'.format(response.status_code))

    return response


def save_daily_average_depth(user_id, depth):
    base_url = get_hub_base_url()
    url = POST_SUMP_AVERAGE_URL.format(base_url, user_id)
    current_date = date.today()
    post_body = {'depth': depth, 'date': str(current_date)}

    response = requests.post(url, data=json.dumps(post_body), headers=DEFAULT_HEADERS)
    logging.info('Saved daily average depth response: {}'.format(response.status_code))

    return response


# TODO: figure out how to do push notifications!!!
def send_alert():
    pass


def send_warning():
    pass
