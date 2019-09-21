import time

from mock import patch

from svc.controllers.controller import DepthController


@patch('svc.controllers.controller.alert_validation')
@patch('svc.controllers.controller.api_requests')
@patch('svc.controllers.controller.get_depth_by_intervals')
@patch('svc.controllers.controller.get_intervals')
class TestController:

    def setup_method(self):
        self.START = time.time()
        self.STOP = time.time()
        self.CONTROLLER = DepthController()

    def test_measure_depth__should_call_get_intervals(self, mock_gpio, mock_depth, mock_request, mock_alert):
        mock_gpio.return_value = (self.START, self.STOP)
        self.CONTROLLER.measure_depth()

        mock_gpio.assert_called()

    def test_measure_depth__should_call_get_depth_by_intervals(self, mock_gpio, mock_depth, mock_request, mock_alert):
        mock_gpio.return_value = (self.START, self.STOP)

        self.CONTROLLER.measure_depth()

        mock_depth.assert_called_with(self.START, self.STOP)

    def test_measure_depth__should_return_depth_calculation(self, mock_gpio, mock_depth, mock_request, mock_alert):
        mock_gpio.return_value = (self.START, self.STOP)
        expected_depth = 1234.332
        mock_depth.return_value = expected_depth

        actual = self.CONTROLLER.measure_depth()

        assert actual == expected_depth

    def test_measure_depth__should_make_api_call_to_save_depth(self, mock_gpio, mock_depth, mock_request, mock_alert):
        expected_depth = 123.45
        mock_gpio.return_value = (self.START, self.STOP)
        mock_depth.return_value = expected_depth

        self.CONTROLLER.measure_depth()

        mock_request.save_current_depth.assert_called_with(None, expected_depth, self.STOP)

    def test_measure_depth__should_call_alert_validation(self, mock_gpio, mock_depth, mock_requests, mock_alert):
        depth = 123.45
        mock_gpio.return_value = (self.START, self.STOP)
        mock_depth.return_value = depth

        self.CONTROLLER.measure_depth()

        mock_alert.assert_called_with(depth, self.CONTROLLER.get_daily_average(), None)

    def test_get_daily_average__should_average_multiple_results(self, mock_gpio, mock_depth, mock_request, mock_alert):
        first_depth = 20.0
        second_depth = 10.0
        mock_gpio.return_value = (self.START, self.STOP)
        mock_depth.side_effect = [first_depth, second_depth]

        self.CONTROLLER.measure_depth()
        self.CONTROLLER.measure_depth()
        actual = self.CONTROLLER.get_daily_average()

        assert actual == 15.0

    def test_get_daily_average__should_default_to_zero_when_not_run_yet(self, mock_gpio, mock_depth, mock_request, mock_alert):
        actual = self.CONTROLLER.get_daily_average()

        assert actual == 0

    def test_get_daily_average__should_default_to_zero_iterated_but_no_depth_measure(self, mock_gpio, mock_depth, mock_request, mock_alert):
        self.CONTROLLER.iteration = 1
        self.CONTROLLER.average_depth = 0

        actual = self.CONTROLLER.get_daily_average()

        assert actual == 0

    def test_save_daily_average__should_call_api_request(self, mock_gpio, mock_depth, mock_request, mock_alert):
        self.CONTROLLER.save_daily_average()

        mock_request.save_daily_average_depth.assert_called_with(self.CONTROLLER.USER_ID, self.CONTROLLER.average_depth)

    def test_save_daily_average__should_reset_objects_depth_and_iteration_tallies(self, mock_gpio, mock_depth, mock_requests, mock_alert):
        self.CONTROLLER.iteration = 23
        self.CONTROLLER.average_depth = 34.12

        self.CONTROLLER.save_daily_average()

        assert self.CONTROLLER.iteration == 0
        assert self.CONTROLLER.average_depth == 0
