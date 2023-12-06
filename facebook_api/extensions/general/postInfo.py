# pylint: skip-file

from typing import Any
from dataclasses import dataclass
import json
@dataclass
class PostInfo:
    like_count: int
    media_url: str
    permalink: str
    timestamp: str
    caption: str
    comments_count: int
    media_type: str
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'PostInfo':
        _like_count = int(obj.get("like_count"))
        _media_url = str(obj.get("media_url"))
        _permalink = str(obj.get("permalink"))
        _timestamp = str(obj.get("timestamp"))
        _caption = str(obj.get("caption"))
        _comments_count = int(obj.get("comments_count"))
        _media_type = str(obj.get("media_type"))
        _id = str(obj.get("id"))
        return PostInfo(_like_count, _media_url, _permalink, _timestamp, _caption, _comments_count, _media_type, _id)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)