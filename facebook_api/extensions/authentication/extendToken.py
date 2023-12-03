from typing import Any
from dataclasses import dataclass
import json
@dataclass
class ExtendToken:
    access_token: str
    token_type: str
    expires_in: int

    @staticmethod
    def from_dict(obj: Any) -> 'ExtendToken':
        _access_token = str(obj.get("access_token"))
        _token_type = str(obj.get("token_type"))
        _expires_in = int(obj.get("expires_in"))
        return ExtendToken(_access_token, _token_type, _expires_in)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
