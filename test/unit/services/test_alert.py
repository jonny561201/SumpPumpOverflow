from mock import patch

from svc.services.alert import calculate_alert


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_exceeds_emergency_threshold(mock_alert):
    depth = 14.0
    daily_average = 674.23
    calculate_alert(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_distance_equal_emergency_threshold(mock_alert):
    depth = 15.0
    daily_average = 637.23
    calculate_alert(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_distance_greater_than_alert_percent_for_daily(mock_alert):
    depth = 200.0
    daily_average = 119.0
    calculate_alert(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_distance_equal_alert_percent_for_daily(mock_alert):
    depth = 200.0
    daily_average = 120.0
    calculate_alert(depth, daily_average, 1000.0)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_distance_greater_than_alert_percent_for_running(mock_alert):
    depth = 200.0
    daily_average = 200.0
    running_average = 119.0
    calculate_alert(depth, daily_average, running_average)

    mock_alert.assert_called()


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_send_alert_when_distance_equal_alert_percent_for_running(mock_alert):
    depth = 200.0
    daily_average = 200.0
    running_average = 120.0
    calculate_alert(depth, daily_average, running_average)

    mock_alert.assert_called()


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_send_warning_when_depth_greater_than_twenty_percent_over_daily_average(mock_warning):
    depth = 200.0
    daily_average = 159.0
    calculate_alert(depth, daily_average, 1000.0)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_send_warning_when_depth_equal_twenty_percent_over_daily_average(mock_warning):
    depth = 200.0
    daily_average = 160.0
    calculate_alert(depth, daily_average, 1000.0)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_not_send_warning_when_fail_multiple_checks(mock_warning):
    depth = 15.0
    daily_average = 10.0
    calculate_alert(depth, daily_average, 1000.0)

    assert mock_warning.call_count == 0


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_send_warning_when_depth_greater_than_twenty_percent_greater_than_running_average(mock_warning):
    depth = 200.0
    daily_average = 200.0
    running_average = 159.0
    calculate_alert(depth, daily_average, running_average)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_send_warning_when_depth_twenty_percent_greater_than_running_average(mock_warning):
    depth = 200.0
    daily_average = 200.0
    running_average = 160.0
    calculate_alert(depth, daily_average, running_average)

    mock_warning.assert_called()


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_not_send_warning_when_distance_above_emergency_threshold(mock_warning):
    depth = 16.0
    daily_average = 637.23
    running_average = 1000.0
    calculate_alert(depth, daily_average, running_average)

    assert not mock_warning.called


@patch('svc.services.alert.send_warning')
def test_calculate_alert__should_not_send_warning_when_depth_less_than_twenty_percent_greater_than_daily_average(mock_warning):
    depth = 200.0
    daily_average = 180.0
    running_average = 1000.0
    calculate_alert(depth, daily_average, running_average)

    assert not mock_warning.called


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_return_warning_level_of_three_when_emergency(mock_alert):
    depth = 14.0
    daily_average = 674.23
    actual = calculate_alert(depth, daily_average, 1000.0)

    assert actual == 3


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_return_warning_level_of_two_when_alert_for_daily(mock_alert):
    depth = 200.0
    daily_average = 119.0
    actual = calculate_alert(depth, daily_average, 1000.0)

    assert actual == 2


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_return_warning_level_of_two_when_alert_for_running(mock_alert):
    depth = 200.0
    daily_average = 200.0
    running_average = 119.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 2


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_return_warning_level_of_one_when_warning_for_running(mock_alert):
    depth = 200.0
    daily_average = 200.0
    running_average = 159.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 1


@patch('svc.services.alert.send_alert')
def test_calculate_alert__should_return_warning_level_of_one_when_warning_for_daily(mock_alert):
    depth = 200.0
    daily_average = 160.0
    actual = calculate_alert(depth, daily_average, 1000.0)

    assert actual == 1


def test_calculate_alert__should_return_warning_level_of_zero_when_not_exceeding_alert_states():
    depth = 200.0
    daily_average = 200.0
    actual = calculate_alert(depth, daily_average, 200.0)

    assert actual == 0

