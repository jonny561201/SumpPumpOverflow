import time

from mock import patch, ANY, MagicMock

from svc.controllers.controller import DepthController, REPORT_INTERVAL, DEPTH_THRESHOLD


@patch('svc.controllers.controller.calculate_alert')
@patch('svc.controllers.controller.api_requests')
@patch('svc.controllers.controller.get_depth_by_intervals')
@patch('svc.controllers.controller.create_gpio')
class TestController:

    def setup_method(self):
        self.START = time.time()
        self.STOP = time.time()

    def _create_controller(self, mock_gpio):
        mock_get_intervals = MagicMock(return_value=(self.START, self.STOP))
        mock_gpio.return_value = mock_get_intervals
        controller = DepthController()
        return controller, mock_get_intervals

    def test_measure_depth__should_call_get_intervals(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, mock_get_intervals = self._create_controller(mock_gpio)

        controller.measure_depth()

        mock_get_intervals.assert_called()

    def test_measure_depth__should_call_get_depth_by_intervals(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)

        controller.measure_depth()

        mock_depth.assert_called_with(self.START, self.STOP)

    def test_measure_depth__should_return_depth_calculation(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        expected_depth = 1234.332
        mock_depth.return_value = expected_depth

        actual = controller.measure_depth()

        assert actual == expected_depth

    def test_measure_depth__should_make_api_call_to_save_depth(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        expected_depth = 123.45
        mock_depth.return_value = expected_depth

        controller.measure_depth()

        mock_request.save_current_depth.assert_called_with(expected_depth, self.STOP, ANY)

    def test_measure_depth__should_make_api_call_to_save_depth_with_alert(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        expected_alert_level = 2
        mock_alert.return_value = expected_alert_level

        controller.measure_depth()

        mock_request.save_current_depth.assert_called_with(ANY, ANY, expected_alert_level)

    def test_measure_depth__should_call_alert_validation(self, mock_gpio, mock_depth, mock_requests, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        depth = 123.45
        mock_depth.return_value = depth

        controller.measure_depth()

        mock_alert.assert_called_with(depth, depth, None)

    def test_measure_depth__should_average_multiple_results_for_alert_validation(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        first_depth = 20.0
        second_depth = 10.0
        mock_depth.side_effect = [first_depth, second_depth]

        controller.measure_depth()
        controller.measure_depth()

        average_depth = (first_depth + second_depth) / 2
        mock_alert.assert_called_with(second_depth, average_depth, None)

    def test_measure_depth__should_default_to_zero_when_iterated_but_no_depth_measurement(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        depth = 0.0
        mock_depth.return_value = depth

        controller.measure_depth()

        mock_alert.assert_called_with(depth, 0, None)

    def test_save_daily_average__should_call_api_request(self, mock_gpio, mock_depth, mock_request, mock_alert):
        controller, _ = self._create_controller(mock_gpio)

        controller.save_daily_average()

        mock_request.save_daily_average_depth.assert_called_with(controller.average_depth)

    def test_save_daily_average__should_reset_objects_depth_and_iteration_tallies(self, mock_gpio, mock_depth, mock_requests, mock_alert):
        controller, _ = self._create_controller(mock_gpio)
        controller.iteration = 23
        controller.average_depth = 34.12

        controller.save_daily_average()

        assert controller.iteration == 0
        assert controller.average_depth == 0


@patch('svc.controllers.controller.create_gpio')
class TestShouldReport:

    def setup_method(self):
        self.base_time = time.time()

    def _create_controller(self, mock_gpio):
        mock_gpio.return_value = MagicMock()
        return DepthController()

    def test_should_report__should_return_true_on_first_reading(self, mock_gpio):
        controller = self._create_controller(mock_gpio)
        assert controller._should_report(100.0, 0, self.base_time) is True

    def test_should_report__should_return_true_when_alert_level_changes(self, mock_gpio):
        controller = self._create_controller(mock_gpio)
        controller.last_reported_depth = 100.0
        controller.last_reported_alert = 0
        controller.last_reported_time = self.base_time

        assert controller._should_report(100.0, 1, self.base_time) is True

    def test_should_report__should_return_true_when_depth_exceeds_threshold(self, mock_gpio):
        controller = self._create_controller(mock_gpio)
        controller.last_reported_depth = 100.0
        controller.last_reported_alert = 0
        controller.last_reported_time = self.base_time

        new_depth = 100.0 + DEPTH_THRESHOLD
        assert controller._should_report(new_depth, 0, self.base_time) is True

    def test_should_report__should_return_true_when_report_interval_elapsed(self, mock_gpio):
        controller = self._create_controller(mock_gpio)
        controller.last_reported_depth = 100.0
        controller.last_reported_alert = 0
        controller.last_reported_time = self.base_time

        elapsed_time = self.base_time + REPORT_INTERVAL
        assert controller._should_report(100.0, 0, elapsed_time) is True

    def test_should_report__should_return_false_when_no_significant_change(self, mock_gpio):
        controller = self._create_controller(mock_gpio)
        controller.last_reported_depth = 100.0
        controller.last_reported_alert = 0
        controller.last_reported_time = self.base_time

        small_change = 100.0 + DEPTH_THRESHOLD - 0.1
        short_time = self.base_time + REPORT_INTERVAL - 1
        assert controller._should_report(small_change, 0, short_time) is False
