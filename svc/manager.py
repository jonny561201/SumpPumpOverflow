from svc.controllers.controller import DepthController
from svc.services.event import MyThread


def create_app(interval_stop_flag, daily_stop_flag):
    controller = DepthController()
    interval_thread = MyThread(interval_stop_flag, controller.measure_depth, 120)
    interval_thread.start()

    daily_thread = MyThread(daily_stop_flag, controller.save_daily_average, 86400)
    daily_thread.start()
