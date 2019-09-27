from threading import Event

from svc.controllers.controller import DepthController
from svc.services.event import MyThread


def create_app():
    interval_stop_flag = Event()
    controller = DepthController()
    MyThread(interval_stop_flag, controller.measure_depth, 120)
