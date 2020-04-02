import json
from datetime import datetime, date

from mock import patch
from requests import Response

from svc.services.api_requests import save_current_depth, save_daily_average_depth


@patch('svc.services.api_requests.get_hub_base_url')
@patch('svc.services.api_requests.date')
@patch('svc.services.api_requests.requests')
class TestApiRequests:
    USER_ID = 'fake_user'
    DEPTH = 12.31
    TIME = 1234556643
    BASE_URL = 'http://fakeurl.com'
    DEFAULT_HEADERS = {'Content-Type': 'text/json'}

    def test_save_current_depth__should_call_request(self, mock_request, mock_date, mock_url):
        mock_url.return_value = self.BASE_URL
        expected_date = datetime.fromtimestamp(self.TIME)
        expected_alert_level = 0
        expected_url = '{}/sumpPump/user/{}/currentDepth'
        expected_data = {'depth': self.DEPTH, 'alert_level': expected_alert_level, 'datetime': str(expected_date)}

        save_current_depth(self.USER_ID, self.DEPTH, self.TIME, expected_alert_level)

        mock_request.post.assert_called_with(expected_url.format(self.BASE_URL, self.USER_ID), data=json.dumps(expected_data), headers=self.DEFAULT_HEADERS)

    def test_save_current_depth__should_return_response(self, mock_request, mock_date, mock_url):
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_current_depth(self.USER_ID, self.DEPTH, self.TIME, 1.1)

        assert actual == response

    def test_save_daily_average_depth__should_call_request(self, mock_request, mock_date, mock_url):
        expected_date = date.today()
        mock_url.return_value = self.BASE_URL
        mock_date.today.return_value = expected_date
        expected_url = '{}/sumpPump/user/{}/averageDepth'
        expected_data = {'depth': self.DEPTH, 'date': str(expected_date)}

        save_daily_average_depth(self.USER_ID, self.DEPTH)

        mock_request.post.assert_called_with(expected_url.format(self.BASE_URL, self.USER_ID), data=json.dumps(expected_data), headers=self.DEFAULT_HEADERS)

    def test_save_daily_average_depth__should_return_response(self, mock_request, mock_date, mock_url):
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_daily_average_depth(self.USER_ID, self.DEPTH)

        assert actual == response
