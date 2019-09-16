from svc.services.api_requests import send_alert, send_warning


EMERGENCY_DEPTH = 15.0
WARNING_PERCENT = 0.2


def alert_validation(depth, daily_average, running_average):
    if depth <= EMERGENCY_DEPTH:
        send_alert()
    elif round(1 - (daily_average / depth), 2) >= WARNING_PERCENT:
        send_warning()
    elif round(1 - (running_average / depth), 2) >= WARNING_PERCENT:
        send_warning()
