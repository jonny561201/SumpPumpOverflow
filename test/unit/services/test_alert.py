from mock import patch

from svc.services.alert import calculate_alert


def test_calculate_alert__should_return_warning_level_of_three_when_below_threshold():
    depth = 14.0
    daily_average = 100.0
    actual = calculate_alert(depth, daily_average, 100.0)

    assert actual == 3


def test_calculate_alert__should_return_warning_level_of_three_when_equal_to_threshold():
    depth = 15.0
    daily_average = 100.0
    actual = calculate_alert(depth, daily_average, 100.0)

    assert actual == 3


def test_calculate_alert__should_return_warning_level_of_two_when_alert_for_daily():
    depth = 60.0
    daily_average = 100.0
    actual = calculate_alert(depth, daily_average, 60.0)

    assert actual == 2


def test_calculate_alert__should_return_warning_level_of_two_when_daily_equal_alert_threshold():
    depth = 60
    daily_average = 84
    actual = calculate_alert(depth, daily_average, 60.0)

    assert actual == 2


def test_calculate_alert__should_return_warning_level_of_two_when_running_equal_alert_threshold():
    depth = 42.857
    daily_average = 84
    actual = calculate_alert(depth, daily_average, 60.0)

    assert actual == 2


def test_calculate_alert__should_return_warning_level_of_two_when_alert_for_running():
    depth = 60.0
    daily_average = 60.0
    running_average = 100.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 2


def test_calculate_alert__should_return_warning_level_of_one_when_warning_for_running():
    depth = 80.0
    daily_average = 80.0
    running_average = 100.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 1


def test_calculate_alert__should_return_warning_level_of_one_when_daily_equals_alert_threshold():
    depth = 80.0
    daily_average = 96.0
    running_average = 80.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 1


def test_calculate_alert__should_return_warning_level_of_one_when_running_equals_alert_threshold():
    depth = 80.0
    daily_average = 80.0
    running_average = 96.0
    actual = calculate_alert(depth, daily_average, running_average)

    assert actual == 1


def test_calculate_alert__should_return_warning_level_of_one_when_warning_for_daily():
    depth = 80.0
    daily_average = 100.0
    actual = calculate_alert(depth, daily_average, 80.0)

    assert actual == 1


def test_calculate_alert__should_return_warning_level_of_zero_when_not_exceeding_alert_states():
    depth = 200.0
    daily_average = 200.0
    actual = calculate_alert(depth, daily_average, 200.0)

    assert actual == 0

