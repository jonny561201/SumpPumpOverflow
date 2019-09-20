from svc.utilities.gpio import get_intervals
from svc.utilities.depth import get_depth_by_intervals
from svc.services.api_requests import save_current_depth
from svc.services.alert import alert_validation

USER_ID = None


# TODO: Make into class to keep a running average of current depth
class DepthController:

    average_depth = 0
    iteration = 0

    def measure_depth(self):
        start, stop = get_intervals()
        depth = get_depth_by_intervals(start, stop)
        save_current_depth(USER_ID, depth, stop)
        self.__update_average_depth(depth)
        alert_validation(depth, self.get_daily_average(), None)

        return depth

    def get_daily_average(self):
        if self.iteration == 0:
            return 0
        return self.average_depth / self.iteration

    def __update_average_depth(self, depth):
        self.average_depth += depth
        self.iteration += 1
