# pylint: skip-file

from typing import Any
from dataclasses import dataclass
import json
@dataclass
class UserAuth:
    access_token: str
    token_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserAuth':
        _access_token = str(obj.get("access_token"))
        _token_type = str(obj.get("token_type"))
        return UserAuth(_access_token, _token_type)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
