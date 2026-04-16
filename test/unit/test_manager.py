from threading import Event

from mock import patch, MagicMock

from svc.manager import create_app


@patch('svc.manager.get_hub_info')
@patch('svc.manager.MyThread')
@patch('svc.manager.DepthController')
class TestManager:
    interval_thread = Event()
    daily_thread = Event()

    def test_create_app__should_create_controller(self, mock_controller, mock_thread, mock_hub_info):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_controller.assert_called()

    def test_create_app__should_create_interval_thread(self, mock_controller, mock_thread, mock_hub_info):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.assert_any_call(self.interval_thread, mock_controller.return_value.measure_depth, 120)

    def test_create_app__should_start_interval_thread(self, mock_controller, mock_thread, mock_hub_info):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.return_value.start.assert_called()

    def test_create_app__should_create_daily_thread(self, mock_controller, mock_thread, mock_hub_info):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.assert_any_call(self.daily_thread, mock_controller.return_value.save_daily_average, 86400)

    def test_create_app__should_start_daily_thread(self, mock_controller, mock_thread, mock_hub_info):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_thread.return_value.start.assert_called()
        assert mock_thread.return_value.start.call_count == 2


@patch('svc.manager.MdnsRegistration')
@patch('svc.manager.wait_for_registration')
@patch('svc.manager.get_hub_info')
@patch('svc.manager.MyThread')
@patch('svc.manager.DepthController')
class TestManagerRegistration:
    interval_thread = Event()
    daily_thread = Event()

    def test_create_app__should_register_mdns_when_no_hub_info(self, mock_controller, mock_thread, mock_hub_info, mock_wait, mock_mdns):
        mock_hub_info.return_value = None
        create_app(self.interval_thread, self.daily_thread)

        mock_mdns.assert_called_with(5002)
        mock_mdns.return_value.register.assert_called()

    def test_create_app__should_wait_for_registration_when_no_hub_info(self, mock_controller, mock_thread, mock_hub_info, mock_wait, mock_mdns):
        mock_hub_info.return_value = None
        create_app(self.interval_thread, self.daily_thread)

        mock_wait.assert_called_with(5002)

    def test_create_app__should_unregister_mdns_after_registration(self, mock_controller, mock_thread, mock_hub_info, mock_wait, mock_mdns):
        mock_hub_info.return_value = None
        create_app(self.interval_thread, self.daily_thread)

        mock_mdns.return_value.unregister.assert_called()

    def test_create_app__should_skip_registration_when_hub_info_exists(self, mock_controller, mock_thread, mock_hub_info, mock_wait, mock_mdns):
        mock_hub_info.return_value = MagicMock()
        create_app(self.interval_thread, self.daily_thread)

        mock_mdns.assert_not_called()
        mock_wait.assert_not_called()
