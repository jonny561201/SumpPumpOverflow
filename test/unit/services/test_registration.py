import json

from mock import patch, MagicMock

from svc.services.registration import _RegistrationHandler


@patch('svc.services.registration.save_hub_info')
class TestRegistrationHandler:
    API_KEY = 'test_key'
    IP_ADDRESS = '192.168.1.50'
    PORT = 5002

    def _create_handler(self, path, body=None):
        handler = object.__new__(_RegistrationHandler)
        handler.path = path
        handler.rfile = MagicMock()
        handler.headers = {'Content-Length': str(len(json.dumps(body))) if body else '0'}
        handler.rfile.read.return_value = json.dumps(body).encode() if body else b''
        handler.server = MagicMock()
        handler.send_response = MagicMock()
        handler.send_header = MagicMock()
        handler.end_headers = MagicMock()
        return handler

    def test_do_post__should_save_registration_data(self, mock_save):
        body = {'api_key': self.API_KEY, 'ip_address': self.IP_ADDRESS, 'port': self.PORT}
        handler = self._create_handler('/register', body)

        handler.do_POST()

        mock_save.assert_called_once()
        saved_data = mock_save.call_args[0][0]
        assert saved_data.api_key == self.API_KEY
        assert saved_data.ip_address == self.IP_ADDRESS
        assert saved_data.port == self.PORT

    def test_do_post__should_set_registration_complete_event(self, mock_save):
        body = {'api_key': self.API_KEY, 'ip_address': self.IP_ADDRESS, 'port': self.PORT}
        handler = self._create_handler('/register', body)

        handler.do_POST()

        handler.server.registration_complete.set.assert_called()

    def test_do_post__should_return_200_on_register(self, mock_save):
        body = {'api_key': self.API_KEY, 'ip_address': self.IP_ADDRESS, 'port': self.PORT}
        handler = self._create_handler('/register', body)

        handler.do_POST()

        handler.send_response.assert_called_with(200)

    def test_do_post__should_return_404_on_unknown_path(self, mock_save):
        handler = self._create_handler('/unknown')

        handler.do_POST()

        handler.send_response.assert_called_with(404)
        mock_save.assert_not_called()
