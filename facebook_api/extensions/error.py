from typing import Any
from dataclasses import dataclass
import json

@dataclass
class Error:
    message: str
    type: str
    code: int
    error_subcode: int
    fbtrace_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        _message        = str(obj.get("message"))
        _type           = str(obj.get("type"))
        _code           = int(obj.get("code"))
        _error_subcode  = obj.get("error_subcode") # this for some reason is a int now was a string before
        _fbtrace_id     = str(obj.get("fbtrace_id"))
        return Error(_message, _type, _code, _error_subcode, _fbtrace_id)

@dataclass
class RequestError:
    error: Error

    @staticmethod
    def from_dict(obj: Any) -> 'RequestError':
        _error = Error.from_dict(obj.get("error"))
        return RequestError(_error)