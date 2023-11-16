from typing import Any
from dataclasses import dataclass
import json
from facebook_api.extensions.error import RequestError



@dataclass
class Me:
    name: str
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Me':
        _name   = str(obj.get("name"))
        _id     = str(obj.get("id"))
        return Me(_name, _id)
    
