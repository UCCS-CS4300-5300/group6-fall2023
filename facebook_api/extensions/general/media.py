from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Cursors:
    before: str
    after: str

    @staticmethod
    def from_dict(obj: Any) -> 'Cursors':
        _before = str(obj.get("before"))
        _after = str(obj.get("after"))
        return Cursors(_before, _after)

@dataclass
class Datum:
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        _id = str(obj.get("id"))
        return Datum(_id)

@dataclass
class Paging:
    cursors: Cursors

    @staticmethod
    def from_dict(obj: Any) -> 'Paging':
        _cursors = Cursors.from_dict(obj.get("cursors"))
        return Paging(_cursors)

@dataclass
class Posts:
    data: List[Datum]
    paging: Paging

    @staticmethod
    def from_dict(obj: Any) -> 'Posts':
        _data = [Datum.from_dict(y) for y in obj.get("data")]
        _paging = Paging.from_dict(obj.get("paging"))
        return Posts(_data, _paging)

