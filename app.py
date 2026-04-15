import logging
from threading import Event

from svc.manager import create_app

logging.basicConfig(filename='sumpPump.log', level=logging.DEBUG)
interval_stop_flag = Event()
daily_stop_flag = Event()


if __name__ == '__main__':
    try:
        logging.info('Application started!')
        create_app(interval_stop_flag, daily_stop_flag)
    except KeyboardInterrupt:
        interval_stop_flag.set()
        daily_stop_flag.set()
        logging.error('Application interrupted by user')
