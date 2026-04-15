import json

from svc.config.settings_state import Settings
from svc.models.registration import RegistrationData


def get_hub_info():
    file_name = Settings.get_instance().hub_info_file
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = json.load(file)
        return RegistrationData.from_dict(content)
    except (FileNotFoundError, KeyError, TypeError):
        return None


def save_hub_info(data: RegistrationData):
    file_name = Settings.get_instance().hub_info_file
    with open(file_name, 'w', encoding='utf-8') as file:
        content = data.to_dict()
        json.dump(content, file)
