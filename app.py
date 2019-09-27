from threading import Event

from svc.manager import create_app

interval_stop_flag = Event()
daily_stop_flag = Event()

try:
    create_app(interval_stop_flag, daily_stop_flag)
except KeyboardInterrupt:
    interval_stop_flag.set()
    daily_stop_flag.set()
    print('Application interrupted by user')
