from svc.services.api_requests import send_alert


EMERGENCY_DEPTH = 15.0
AVERAGE_THRESHOLD_PERCENT = 0.2


def alert_validation(depth, running_average):
    if depth <= EMERGENCY_DEPTH:
        send_alert()
    if round(1 - (running_average / depth), 2) >= AVERAGE_THRESHOLD_PERCENT:
        send_alert()
