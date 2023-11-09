from .utils.constants import facebook_versions


class facebook_Config:
    '''
    Facebook API configuration class for the wrapper.
    '''

    api_version: facebook_versions = facebook_versions["latest"]

    def __init__(self, api_version: facebook_versions = facebook_versions["latest"]):
        self.api_version = api_version

    def set_version(self, version: facebook_versions):
        '''
        set the api version for the wrapper
        '''
        self.api_version = version


