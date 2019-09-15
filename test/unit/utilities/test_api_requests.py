import json
from datetime import datetime

from mock import patch

from svc.utilities.api_requests import save_current_daily_depth


@patch('svc.utilities.api_requests.requests')
def test_save_current_daily_depth__should_call_request(mock_request):
    user_id = 'fake_user'
    depth = 12.31
    time = 1234556643
    date = datetime.fromtimestamp(time)
    expected_url = 'http://localhost:8080/sumpPump/user/' + user_id + '/currentDepth'
    expected_data = json.dumps({'depth': depth, 'datetime': str(date)})

    save_current_daily_depth(user_id, depth, time)

    mock_request.post.assert_called_with(expected_url, data=expected_data)
