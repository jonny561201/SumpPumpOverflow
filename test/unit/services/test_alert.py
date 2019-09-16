from mock import patch

from svc.services.alert import alert_validation


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_call_send_alert_when_exceeds_emergency_threshold(mock_alert):
    depth = 14.0
    daily_average = 674.23
    alert_validation(depth, daily_average, None)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_distance_equal_emergency_threshold(mock_alert):
    depth = 15.0
    daily_average = 637.23
    alert_validation(depth, daily_average, None)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_depth_greater_than_twenty_percent_over_daily_average(mock_alert):
    depth = 200.0
    daily_average = 159.0
    alert_validation(depth, daily_average, None)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_depth_equal_twenty_percent_over_daily_average(mock_alert):
    depth = 200.0
    daily_average = 160.0
    alert_validation(depth, daily_average, None)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_not_send_alert_twice_when_fail_multiple_checks(mock_alert):
    depth = 15.0
    daily_average = 10.0
    alert_validation(depth, daily_average, None)

    assert mock_alert.call_count == 1


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_depth_twenty_percent_greater_than_running_average(mock_alert):
    depth = 200.0
    daily_average = 200.0
    running_average = 159.0
    alert_validation(depth, daily_average, running_average)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_not_send_alert_when_distance_above_emergency_threshold(mock_alert):
    depth = 16.0
    daily_average = 637.23
    running_average = 1000.0
    alert_validation(depth, daily_average, running_average)

    assert not mock_alert.called


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_not_send_alert_when_depth_less_than_twenty_percent_greater_than_daily_average(
        mock_alert):
    depth = 200.0
    daily_average = 180.0
    running_average = 1000.0
    alert_validation(depth, daily_average, running_average)

    assert not mock_alert.called
