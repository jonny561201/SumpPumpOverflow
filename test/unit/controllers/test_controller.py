import time

from mock import patch

from svc.controllers.controller import measure_depth


@patch('svc.controllers.controller.save_current_daily_depth')
@patch('svc.controllers.controller.get_depth_by_intervals')
@patch('svc.controllers.controller.get_intervals')
class TestController:

    def setup_method(self):
        self.START = time.time()
        self.STOP = time.time()

    def test_measure_depth__should_call_get_intervals(self, mock_gpio, mock_depth, mock_request):
        mock_gpio.return_value = (self.START, self.STOP)
        measure_depth()

        mock_gpio.assert_called()

    def test_measure_depth__should_call_get_depth_by_intervals(self, mock_gpio, mock_depth, mock_request):
        mock_gpio.return_value = (self.START, self.STOP)

        measure_depth()

        mock_depth.assert_called_with(self.START, self.STOP)

    def test_measure_depth__should_return_depth_calculation(self, mock_gpio, mock_depth, mock_request):
        mock_gpio.return_value = (self.START, self.STOP)
        expected_depth = 1234.332
        mock_depth.return_value = expected_depth

        actual = measure_depth()

        assert actual == expected_depth

    def test_measure_depth__should_make_api_call_to_save(self, mock_gpio, mock_depth, mock_request):
        expected_depth = 123.45
        mock_gpio.return_value = (self.START, self.STOP)
        mock_depth.return_value = expected_depth

        measure_depth()

        mock_request.assert_called_with(expected_depth, self.STOP)
