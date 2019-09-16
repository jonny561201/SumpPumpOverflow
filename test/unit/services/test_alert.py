from mock import patch

from svc.services.alert import alert_validation


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_call_send_alert_when_exceeds_emergency_threshold(mock_alert):
    depth = 14.0
    daily_average = 674.23
    alert_validation(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_distance_equal_emergency_threshold(mock_alert):
    depth = 15.0
    daily_average = 637.23
    alert_validation(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_alert_validation__should_send_alert_when_distance_greater_than_alert_percent(mock_alert):
    depth = 200.0
    daily_average = 119.0
    alert_validation(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_send_warning_when_depth_greater_than_twenty_percent_over_daily_average(mock_warning):
    depth = 200.0
    daily_average = 159.0
    alert_validation(depth, daily_average, 1000.0)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_send_warning_when_depth_equal_twenty_percent_over_daily_average(mock_warning):
    depth = 200.0
    daily_average = 160.0
    alert_validation(depth, daily_average, 1000.0)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_not_send_warning_when_fail_multiple_checks(mock_warning):
    depth = 15.0
    daily_average = 10.0
    alert_validation(depth, daily_average, 1000.0)

    assert mock_warning.call_count == 0


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_send_warning_when_depth_greater_than_twenty_percent_greater_than_running_average(mock_warning):
    depth = 200.0
    daily_average = 200.0
    running_average = 159.0
    alert_validation(depth, daily_average, running_average)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_send_warning_when_depth_twenty_percent_greater_than_running_average(mock_warning):
    depth = 200.0
    daily_average = 200.0
    running_average = 160.0
    alert_validation(depth, daily_average, running_average)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_not_send_warning_when_distance_above_emergency_threshold(mock_warning):
    depth = 16.0
    daily_average = 637.23
    running_average = 1000.0
    alert_validation(depth, daily_average, running_average)

    assert not mock_warning.called


@patch('svc.services.alert.send_warning')
def test_alert_validation__should_not_send_warning_when_depth_less_than_twenty_percent_greater_than_daily_average(
        mock_warning):
    depth = 200.0
    daily_average = 180.0
    running_average = 1000.0
    alert_validation(depth, daily_average, running_average)

    assert not mock_warning.called


