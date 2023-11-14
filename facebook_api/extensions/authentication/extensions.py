from ...request_base import request_base
from ...extensions.authentication.userAuth import UserAuth
class general:
    '''
    general extension for the facebook api wrapper
    '''
    request: request_base = None  # our request base for easy typing

    # init our extension base
    def __init__(self, base: request_base) -> None:
        self.request = base
