# pylint: skip-file

from typing import Any
from dataclasses import dataclass
import json




@dataclass
class InstagramBusinessAccount:
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'InstagramBusinessAccount':
        _id = str(obj.get("id"))
        return InstagramBusinessAccount(_id)

@dataclass
class BusinessAccounts:
    instagram_business_account: InstagramBusinessAccount
    id: str

    @staticmethod
    def from_dict(obj: Any) -> 'BusinessAccounts':
        _instagram_business_account = InstagramBusinessAccount.from_dict(obj.get("instagram_business_account"))
        _id = str(obj.get("id"))
        return BusinessAccounts(_instagram_business_account, _id)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
