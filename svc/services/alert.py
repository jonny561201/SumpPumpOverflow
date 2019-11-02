from svc.services.api_requests import send_alert, send_warning


EMERGENCY_DEPTH = 15.0
WARNING_PERCENT = 0.2
ALERT_PERCENT = 0.4


def alert_validation(depth, daily_average, running_average):
    alert_level = 0
    percent_of_daily = round(1 - (daily_average / depth), 2)
    percent_of_running = round(1 - (running_average / depth), 2)

    if depth <= EMERGENCY_DEPTH:
        send_alert()
        alert_level = 3
    elif percent_of_daily >= ALERT_PERCENT:
        send_alert()
        alert_level = 2
    elif percent_of_running >= ALERT_PERCENT:
        send_alert()
    elif percent_of_daily >= WARNING_PERCENT:
        send_warning()
    elif percent_of_running >= WARNING_PERCENT:
        send_warning()

    return alert_level
