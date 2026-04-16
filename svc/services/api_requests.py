import logging
from datetime import datetime, date, timezone

import requests

from svc.utilities.file_utils import get_hub_info


def save_current_depth(depth, time, alert_level):
    hub = get_hub_info()
    url = f'http://{hub.ip_address}:{hub.port}/sumpPump/currentDepth'
    headers = {'X-API-Key': hub.api_key, 'Content-Type': 'application/json'}
    current_time = datetime.fromtimestamp(time, tz=timezone.utc)
    post_body = {'depth': depth, 'alert_level': alert_level, 'datetime': current_time.isoformat()}

    response = requests.post(url, json=post_body, headers=headers)
    logging.info('Saved current depth response: {}'.format(response.status_code))

    return response


def save_daily_average_depth(depth):
    hub = get_hub_info()
    url = f'http://{hub.ip_address}:{hub.port}/sumpPump/averageDepth'
    headers = {'X-API-Key': hub.api_key, 'Content-Type': 'application/json'}
    current_date = date.today()
    post_body = {'depth': depth, 'date': str(current_date)}

    response = requests.post(url, json=post_body, headers=headers)
    logging.info('Saved daily average depth response: {}'.format(response.status_code))

    return response


# TODO: figure out how to do push notifications!!!
def send_alert():
    pass


def send_warning():
    pass
