# pylint: skip-file

from typing import Any
from dataclasses import dataclass
import json
@dataclass
class BasicProfileMetrics:
    id: str
    username: str
    media_count: int
    followers_count: int
    follows_count: int
    name: str
    biography: str
    profile_picture_url: str

    @staticmethod
    def from_dict(obj: Any) -> 'BasicProfileMetrics':
        _id = str(obj.get("id"))
        _username = str(obj.get("username"))
        _media_count = int(obj.get("media_count"))
        _followers_count = int(obj.get("followers_count"))
        _follows_count = int(obj.get("follows_count"))
        _name = str(obj.get("name"))
        _biography = str(obj.get("biography"))
        _profile_picture_url = str(obj.get("profile_picture_url"))
        return BasicProfileMetrics(_id, _username, _media_count, _followers_count, _follows_count, _name, _biography, _profile_picture_url)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
