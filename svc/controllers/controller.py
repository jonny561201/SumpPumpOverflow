import logging

from svc.services import api_requests
from svc.services.alert import alert_validation
from svc.utilities.depth import get_depth_by_intervals
from svc.utilities.gpio import get_intervals


class DepthController:
    USER_ID = None
    AVERAGE_DEPTH = 0
    ITERATION = 0

    def measure_depth(self):
        start, stop = get_intervals()
        current_depth = get_depth_by_intervals(start, stop)
        logging.info('Current depth: {}'.format(current_depth))

        self.__update_average_depth(current_depth)
        alert_validation(current_depth, self.__get_daily_average(), None)
        api_requests.save_current_depth(self.USER_ID, current_depth, stop)

        return current_depth

    def save_daily_average(self):
        logging.info('Recording Daily Average depth: {}'.format(self.AVERAGE_DEPTH))
        api_requests.save_daily_average_depth(self.USER_ID, self.AVERAGE_DEPTH)
        self.AVERAGE_DEPTH = 0
        self.ITERATION = 0

    def __get_daily_average(self):
        return 0 if self.ITERATION == 0 else self.AVERAGE_DEPTH / self.ITERATION

    def __update_average_depth(self, depth):
        self.AVERAGE_DEPTH += depth
        self.ITERATION += 1
