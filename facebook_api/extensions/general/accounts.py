# pylint: skip-file

from typing import List, Any
from dataclasses import dataclass

@dataclass
class CategoryList:
    id: str
    name: str

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryList':
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        return CategoryList(_id, _name)

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
    access_token: str
    category: str
    category_list: List[CategoryList]
    name: str
    id: str
    tasks: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        _access_token = str(obj.get("access_token"))
        _category = str(obj.get("category"))
        _category_list = [CategoryList.from_dict(y) for y in obj.get("category_list")]
        _name = str(obj.get("name"))
        _id = str(obj.get("id"))
        _tasks = [str(task) for task in obj.get("tasks")]
        return Datum(_access_token, _category, _category_list, _name, _id, _tasks)

@dataclass
class Paging:
    cursors: Cursors

    @staticmethod
    def from_dict(obj: Any) -> 'Paging':
        _cursors = Cursors.from_dict(obj.get("cursors"))
        return Paging(_cursors)

@dataclass
class Accounts:
    data: List[Datum]
    paging: Paging

    @staticmethod
    def from_dict(obj: Any) -> 'Accounts':
        _data = [Datum.from_dict(y) for y in obj.get("data")]
        _paging = Paging.from_dict(obj.get("paging"))
        return Accounts(_data, _paging)
