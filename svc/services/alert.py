from svc.services.api_requests import send_alert


EMERGENCY_DEPTH = 15.0


def alert_validation(depth, running_average):
    if depth <= EMERGENCY_DEPTH:
        send_alert()
    if (running_average / depth) < 0.8:
        send_alert()