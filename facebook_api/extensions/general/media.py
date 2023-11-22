from typing import List
from typing import Any
from dataclasses import dataclass
import json
from ...request_base import request_base
# @dataclass
# class Cursors:
#     before: str
#     after: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Cursors':
#         _before = str(obj.get("before"))
#         _after = str(obj.get("after"))
#         return Cursors(_before, _after)

# @dataclass
# class Datum:
#     id: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Datum':
#         _id = str(obj.get("id"))
#         return Datum(_id)
    
#     # def set_client(self, client: request_base):
#     #     self.client = client

#     # def get_info(self):
#     #     return "test"

# @dataclass
# class Paging:
#     cursors: Cursors

#     @staticmethod
#     def from_dict(obj: Any) -> 'Paging':
#         _cursors = Cursors.from_dict(obj.get("cursors"))
#         return Paging(_cursors)

# @dataclass
# class Posts:
#     data: List[Datum]
#     paging: Paging

#     @staticmethod
#     def from_dict(obj: Any) -> 'Posts':
#         _data = [Datum.from_dict(y) for y in obj.get("data")]
#         _paging = Paging.from_dict(obj.get("paging"))
#         return Posts(_data, _paging)
    
#     # def set_client(self, client: request_base):
#     #     '''
#     #     i would abstract this to a base class that all the data classes inherit from
#     #     but i dont want to confuse anyone on what this is doing so i will just leave it here
#     #     this essentially allows us to later refactor and make this a class that can call requests
#     #     so we dont have to supply ids or object we can just call the posts = get_posts() then get the post index
#     #     and then call posts.data[0].get_info() and it will return the info for that post
#     #     '''
#     #     self.client = client
#     #     for x in self.data:
#     #         x.set_client(client)


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

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
