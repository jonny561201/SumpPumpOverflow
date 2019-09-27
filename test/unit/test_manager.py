from mock import patch

from svc.manager import create_app


@patch('svc.manager.DepthController')
def test_create_app__should_create_controller(mock_controller):
    create_app()

    mock_controller.assert_called()
