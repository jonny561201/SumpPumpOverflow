import logging

from svc.services import api_requests
from svc.services.alert import calculate_alert
from svc.utilities.depth import get_depth_by_intervals
from svc.utilities.gpio_factory import create_gpio


REPORT_INTERVAL = 3600
DEPTH_THRESHOLD = 2.0


class DepthController:
    def __init__(self):
        self.average_depth = 0
        self.iteration = 0
        self.last_reported_depth = None
        self.last_reported_alert = 0
        self.last_reported_time = None
        self._get_intervals = create_gpio()

    def measure_depth(self):
        start, stop = self._get_intervals()
        current_depth = get_depth_by_intervals(start, stop)
        logging.info('Current depth: {}'.format(current_depth))

        self._update_average_depth(current_depth)
        alert_level = calculate_alert(current_depth, self._get_daily_average(), None)

        if self._should_report(current_depth, alert_level, stop):
            api_requests.save_current_depth(current_depth, stop, alert_level)
            self.last_reported_depth = current_depth
            self.last_reported_alert = alert_level
            self.last_reported_time = stop

        return current_depth

    def save_daily_average(self):
        logging.info('Recording Daily Average depth: {}'.format(self.average_depth))
        api_requests.save_daily_average_depth(self.average_depth)
        self.average_depth = 0
        self.iteration = 0

    def _should_report(self, depth, alert_level, time):
        if self.last_reported_depth is None:
            return True
        if alert_level != self.last_reported_alert:
            return True
        if time - self.last_reported_time >= REPORT_INTERVAL:
            return True
        return abs(depth - self.last_reported_depth) >= DEPTH_THRESHOLD

    def _get_daily_average(self):
        return 0 if self.iteration == 0 else self.average_depth / self.iteration

    def _update_average_depth(self, depth):
        self.average_depth += depth
        self.iteration += 1
