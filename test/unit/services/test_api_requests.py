from datetime import datetime, date, timezone

from mock import patch, MagicMock
from requests import Response

from svc.services.api_requests import save_current_depth, save_daily_average_depth


@patch('svc.services.api_requests.get_hub_info')
@patch('svc.services.api_requests.date')
@patch('svc.services.api_requests.requests')
class TestApiRequests:
    DEPTH = 12.31
    TIME = 1234556643
    API_KEY = 'fake_api_key'
    IP_ADDRESS = '192.168.1.50'
    PORT = 5002

    def _mock_hub(self, mock_hub_info):
        hub = MagicMock()
        hub.api_key = self.API_KEY
        hub.ip_address = self.IP_ADDRESS
        hub.port = self.PORT
        mock_hub_info.return_value = hub
        return hub

    def test_save_current_depth__should_call_request(self, mock_request, mock_date, mock_hub_info):
        self._mock_hub(mock_hub_info)
        expected_time = datetime.fromtimestamp(self.TIME, tz=timezone.utc)
        expected_alert_level = 0
        expected_url = f'http://{self.IP_ADDRESS}:{self.PORT}/sumpPump/currentDepth'
        expected_headers = {'X-API-Key': self.API_KEY, 'Content-Type': 'application/json'}
        expected_data = {'depth': self.DEPTH, 'alert_level': expected_alert_level, 'datetime': expected_time.isoformat()}

        save_current_depth(self.DEPTH, self.TIME, expected_alert_level)

        mock_request.post.assert_called_with(expected_url, json=expected_data, headers=expected_headers, timeout=2)

    def test_save_current_depth__should_return_response(self, mock_request, mock_date, mock_hub_info):
        self._mock_hub(mock_hub_info)
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_current_depth(self.DEPTH, self.TIME, 1.1)

        assert actual == response

    def test_save_daily_average_depth__should_call_request(self, mock_request, mock_date, mock_hub_info):
        self._mock_hub(mock_hub_info)
        expected_date = date.today()
        mock_date.today.return_value = expected_date
        expected_url = f'http://{self.IP_ADDRESS}:{self.PORT}/sumpPump/averageDepth'
        expected_headers = {'X-API-Key': self.API_KEY, 'Content-Type': 'application/json'}
        expected_data = {'depth': self.DEPTH, 'date': str(expected_date)}

        save_daily_average_depth(self.DEPTH)

        mock_request.post.assert_called_with(expected_url, json=expected_data, headers=expected_headers, timeout=2)

    def test_save_daily_average_depth__should_return_response(self, mock_request, mock_date, mock_hub_info):
        self._mock_hub(mock_hub_info)
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_daily_average_depth(self.DEPTH)

        assert actual == response
