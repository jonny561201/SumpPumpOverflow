from threading import Event

from svc.controllers.controller import DepthController
from svc.services.event import MyThread


def create_app():
    interval_stop_flag = Event()
    daily_stop_flag = Event()

    controller = DepthController()
    interval_thread = MyThread(interval_stop_flag, controller.measure_depth, 120)
    interval_thread.start()

    MyThread(daily_stop_flag, controller.save_daily_average, 720)
