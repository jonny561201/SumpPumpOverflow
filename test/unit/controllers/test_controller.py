from mock import patch

from svc.controllers.controller import measure_depth


@patch('svc.controllers.controller.get_intervals')
def test_measure_depth__should_call_get_interval(mock_gpio):
    measure_depth()

    mock_gpio.assert_called()
