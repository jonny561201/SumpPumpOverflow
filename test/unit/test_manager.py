from mock import patch, ANY

from svc.manager import create_app


@patch('svc.manager.MyThread')
@patch('svc.manager.DepthController')
class TestManager:

    def test_create_app__should_create_controller(self, mock_controller, mock_thread):
        create_app()

        mock_controller.assert_called()

    def test_create_app__should_create_daily_interval_thread(self, mock_controller, mock_thread):
        create_app()

        mock_thread.assert_called_with(ANY, mock_controller.return_value.measure_depth, 120)

    def test_create_app__should_start_daily_interval_thread(self, mock_controller, mock_thread):
        create_app()

        mock_thread.return_value.start.assert_called()
