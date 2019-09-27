from threading import Event

from mock import patch

from svc.manager import create_app


@patch('svc.manager.MyThread')
@patch('svc.manager.DepthController')
class TestManager:
    interval_thread = Event()
    daily_thread = Event()

    def test_create_app__should_create_controller(self, mock_controller, mock_thread):
        create_app(self.interval_thread, self.daily_thread)

        mock_controller.assert_called()

    def test_create_app__should_create_interval_thread(self, mock_controller, mock_thread):
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.assert_any_call(self.interval_thread, mock_controller.return_value.measure_depth, 120)

    def test_create_app__should_start_interval_thread(self, mock_controller, mock_thread):
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.return_value.start.assert_called()

    def test_create_app__should_create_daily_thread(self, mock_controller, mock_thread):
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.assert_any_call(self.daily_thread, mock_controller.return_value.save_daily_average, 86400)

    def test_create_app__should_start_daily_thread(self, mock_controller, mock_thread):
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.return_value.start.assert_called()
        assert mock_thread.return_value.start.call_count == 2
