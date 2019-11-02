import json
from datetime import datetime, date

from mock import patch
from requests import Response

from svc.services.api_requests import save_current_depth, save_daily_average_depth


@patch('svc.services.api_requests.date')
@patch('svc.services.api_requests.requests')
class TestApiRequests:
    USER_ID = 'fake_user'
    DEPTH = 12.31
    TIME = 1234556643
    DEFAULT_HEADERS = {'Content-Type': 'text/json'}

    def test_save_current_depth__should_call_request(self, mock_request, mock_date):
        expected_date = datetime.fromtimestamp(self.TIME)
        expected_url = 'http://localhost:8080/sumpPump/user/{}/currentDepth'
        expected_data = {'depth': self.DEPTH, 'datetime': str(expected_date)}

        save_current_depth(self.USER_ID, self.DEPTH, self.TIME)

        mock_request.post.assert_called_with(expected_url.format(self.USER_ID), data=json.dumps(expected_data), headers=self.DEFAULT_HEADERS)

    def test_save_current_depth__should_return_response(self, mock_request, mock_date):
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_current_depth(self.USER_ID, self.DEPTH, self.TIME)

        assert actual == response

    def test_save_daily_average_depth__should_call_request(self, mock_request, mock_date):
        expected_date = date.today()
        mock_date.today.return_value = expected_date
        expected_url = 'http://localhost:8080/sumpPump/user/{}/averageDepth'
        expected_data = {'depth': self.DEPTH, 'date': str(expected_date)}

        save_daily_average_depth(self.USER_ID, self.DEPTH)

        mock_request.post.assert_called_with(expected_url.format(self.USER_ID), data=json.dumps(expected_data), headers=self.DEFAULT_HEADERS)

    def test_save_daily_average_depth__should_return_response(self, mock_request, mock_date):
        response = Response()
        response.status_code = 200
        mock_request.post.return_value = response

        actual = save_daily_average_depth(self.USER_ID, self.DEPTH)

        assert actual == response
