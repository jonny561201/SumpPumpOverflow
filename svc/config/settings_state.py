import json
import os

from svc.config.singleton import Singleton


@Singleton
class Settings:
    _settings = None

    def __init__(self):
        self.__load_settings()
        self.BaseUrls = BaseUrls(self._settings)

    @property
    def environment(self):
        return self._settings.get('Environment', 'local') if self._settings is not None else 'local'

    @property
    def api_key_file(self):
        return self._settings.get('ApiKeyFile') if self._settings is not None else 'apiKey.json'

    def __load_settings(self):
        try:
            environment = os.environ.get('PYTHON_ENVIRONMENT', 'local')
            file_path = os.path.join(os.path.dirname(__file__), '..', '..', f'settings.{environment}.json')
            with open(file_path, "r") as reader:
                self._settings = json.loads(reader.read())
        except Exception:
            self._settings = {}


class BaseUrls:

    def __init__(self, settings):
        self._settings = settings.get('BaseURls', {}) if settings is not None else {}

    @property
    def api_hub(self):
        return self._settings.get('ApiHub')