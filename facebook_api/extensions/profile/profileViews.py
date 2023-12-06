from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Value:
    value: int
    end_time: str

    @staticmethod
    def from_dict(obj: Any) -> 'Value':
        _value = int(obj.get("value"))
        _end_time = str(obj.get("end_time"))
        return Value(_value, _end_time)

@dataclass
class Datum:
    name: str
    period: str
    values: List[Value]
    title: str
    description: str
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        _name = str(obj.get("name"))
        _period = str(obj.get("period"))
        _values = [Value.from_dict(y) for y in obj.get("values")]
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _id = str(obj.get("id"))
        return Datum(_name, _period, _values, _title, _description, _id)

@dataclass
class Paging:
    previous: str
    next: str

    @staticmethod
    def from_dict(obj: Any) -> 'Paging':
        _previous = str(obj.get("previous"))
        _next = str(obj.get("next"))
        return Paging(_previous, _next)

@dataclass
class ProfileViews:
    data: List[Datum]
    paging: Paging

    @staticmethod
    def from_dict(obj: Any) -> 'ProfileViews':
        _data = [Datum.from_dict(y) for y in obj.get("data")]
        _paging = Paging.from_dict(obj.get("paging"))
        return ProfileViews(_data, _paging)



# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
