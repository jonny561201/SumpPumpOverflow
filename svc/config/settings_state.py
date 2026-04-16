import json
import os

from svc.config.singleton import Singleton


@Singleton
class Settings:
    _settings = None

    def __init__(self):
        self.__load_settings()

    @property
    def environment(self):
        return self._settings.get('Environment', 'local') if self._settings is not None else 'local'

    @property
    def hub_info_file(self):
        return self._settings.get('HubInfoFile') if self._settings is not None else 'apiKey.json'

    def __load_settings(self):
        environment = os.environ.get('PYTHON_ENVIRONMENT', 'local')
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', f'settings.{environment}.json')
        with open(file_path, "r") as reader:
            self._settings = json.loads(reader.read())