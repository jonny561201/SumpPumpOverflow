import json

from mock import patch, mock_open

from svc.utilities.file_utils import get_hub_info, save_hub_info
from svc.models.registration import RegistrationData


@patch('svc.utilities.file_utils.Settings')
class TestGetHubInfo:
    FILE_NAME = '/home/pi/hubInfo.json'
    API_KEY = 'test_api_key'
    IP_ADDRESS = '192.168.1.100'
    PORT = 5002

    def _mock_settings(self, mock_settings):
        mock_settings.get_instance.return_value.hub_info_file = self.FILE_NAME

    def test_get_hub_info__should_return_registration_data(self, mock_settings):
        self._mock_settings(mock_settings)
        file_content = json.dumps({'api_key': self.API_KEY, 'ip_address': self.IP_ADDRESS, 'port': self.PORT})

        with patch('builtins.open', mock_open(read_data=file_content)):
            result = get_hub_info()

        assert result.api_key == self.API_KEY
        assert result.ip_address == self.IP_ADDRESS
        assert result.port == self.PORT

    def test_get_hub_info__should_return_none_when_file_not_found(self, mock_settings):
        self._mock_settings(mock_settings)

        with patch('builtins.open', side_effect=FileNotFoundError):
            result = get_hub_info()

        assert result is None

    def test_get_hub_info__should_return_none_when_file_has_missing_keys(self, mock_settings):
        self._mock_settings(mock_settings)
        file_content = json.dumps({'api_key': self.API_KEY})

        with patch('builtins.open', mock_open(read_data=file_content)):
            result = get_hub_info()

        assert result is None


@patch('svc.utilities.file_utils.Settings')
class TestSaveHubInfo:
    FILE_NAME = '/home/pi/hubInfo.json'

    def _mock_settings(self, mock_settings):
        mock_settings.get_instance.return_value.hub_info_file = self.FILE_NAME

    def test_save_hub_info__should_write_registration_data_to_file(self, mock_settings):
        self._mock_settings(mock_settings)
        data = RegistrationData(api_key='key123', ip_address='10.0.0.1', port=8080)
        m = mock_open()

        with patch('builtins.open', m):
            save_hub_info(data)

        m.assert_called_with(self.FILE_NAME, 'w', encoding='utf-8')
        written = m().write.call_args_list
        written_content = ''.join(call.args[0] for call in written)
        parsed = json.loads(written_content)
        assert parsed == {'api_key': 'key123', 'ip_address': '10.0.0.1', 'port': 8080}
