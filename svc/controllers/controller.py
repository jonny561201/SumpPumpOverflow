from svc.utilities.gpio import get_intervals
from svc.utilities.depth import get_depth_by_intervals
from svc.services import api_requests
from svc.services.alert import alert_validation


class DepthController:

    USER_ID = None
    AVERAGE_DEPTH = 0
    ITERATION = 0

    def measure_depth(self):
        start, stop = get_intervals()
        current_depth = get_depth_by_intervals(start, stop)
        api_requests.save_current_depth(self.USER_ID, current_depth, stop)
        self.__update_average_depth(current_depth)
        alert_validation(current_depth, self._get_daily_average(), None)

        return current_depth

    def save_daily_average(self):
        api_requests.save_daily_average_depth(self.USER_ID, self.AVERAGE_DEPTH)
        self.AVERAGE_DEPTH = 0
        self.ITERATION = 0

    def _get_daily_average(self):
        return 0 if self.ITERATION == 0 else self.AVERAGE_DEPTH / self.ITERATION

    def __update_average_depth(self, depth):
        self.AVERAGE_DEPTH += depth
        self.ITERATION += 1
