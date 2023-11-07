'''
extensions are used to add new functionality to the api wrapper without having to put it in the main codebase.
'''

from facebook_settings import facebook_Config
from request_base import request_base
from extensions.general.me import Me
from extensions.error import RequestError

class general:
    '''
    general extension for the facebook api wrapper
    '''
    request: request_base = None # our request base for easy typing

    # init our extension base
    def __init__(self, base: request_base) -> None:
        self.request = base

    def get_me(self) -> Me | RequestError:
        '''
        get the current user from facebook that the token is for
        '''
        return self.request.get(self.request.facebook_config.api_version + '/me', object_return_type=Me)
        
    # ... add more extensions here