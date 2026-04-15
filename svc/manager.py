from svc.controllers.controller import DepthController
from svc.services.event import MyThread
from svc.services.registration import wait_for_registration
from svc.utilities.file_utils import get_hub_info
from svc.utilities.mdns_utlity import MdnsRegistration


REGISTRATION_PORT = 5002


def create_app(interval_stop_flag, daily_stop_flag):
    if get_hub_info() is None:
        mdns = MdnsRegistration(REGISTRATION_PORT)
        mdns.register()
        wait_for_registration(REGISTRATION_PORT)
        mdns.unregister()

    controller = DepthController()
    interval_thread = MyThread(interval_stop_flag, controller.measure_depth, 120)
    interval_thread.start()

    daily_thread = MyThread(daily_stop_flag, controller.save_daily_average, 86400)
    daily_thread.start()
