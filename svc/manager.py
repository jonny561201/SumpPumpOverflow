from svc.controllers.controller import DepthController
from svc.services.event import MyThread
from svc.utilities.mdns_utlity import MdnsRegistration


REGISTRATION_PORT = 5002


def create_app(interval_stop_flag, daily_stop_flag):
    mdns = MdnsRegistration(REGISTRATION_PORT)
    mdns.register()

    controller = DepthController()
    interval_thread = MyThread(interval_stop_flag, controller.measure_depth, 120)
    interval_thread.start()

    daily_thread = MyThread(daily_stop_flag, controller.save_daily_average, 86400)
    daily_thread.start()
