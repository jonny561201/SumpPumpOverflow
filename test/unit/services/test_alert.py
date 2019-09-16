from mock import patch

from svc.services.alert import alert_validation


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_call_send_alert_when_exceeds_emergency_threshold(mock_alert):
    depth = 14.0
    running_average = 674.23
    alert_validation(depth, running_average)

    mock_alert.assert_called()
