from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RegistrationData:
    api_key: str
    ip_address: str
    port: int