import time

from mock import patch

from svc.controllers.controller import measure_depth


@patch('svc.controllers.controller.get_depth_by_intervals')
@patch('svc.controllers.controller.get_intervals')
class TestController:

    def setup_method(self):
        self.START = time.time()
        self.STOP = time.time()

    def test_measure_depth__should_call_get_intervals(self, mock_gpio, mock_depth):
        mock_gpio.return_value = (self.START, self.STOP)
        measure_depth()

        mock_gpio.assert_called()

    def test_measure_depth__should_call_get_depth_by_intervals(self, mock_gpio, mock_depth):
        mock_gpio.return_value = (self.START, self.STOP)

        measure_depth()

        mock_depth.assert_called_with(self.START, self.STOP)
