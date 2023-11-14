from .request_base import request_base
from .facebook_settings import facebook_Config
from .utils.constants import BASE_URL
from .extensions.general.extension import general

class facebook_API(request_base):
    '''
    Facebook API class for the wrapper.
    This technically references the request_base.py where the abstracted methods are for REST
    This is the main parent class that you should mess wth. 
    This contains our extensions and other child functions that 
    pertain to the facebook API
    '''

    token: str = None



    def __init__(self, token: str, facebook_config: facebook_Config):
        '''
        Init the class giving it the TOKEN for the user and a FACEBOOK_CONFIG for other settings
        '''
        # init our request base
        super().__init__(facebook_config)

        # set our token and config
        self.token              = token
        self.facebook_config    = facebook_config
        self.required_params    = {'access_token': self.token}

        # init our extensions
        self.general = general(self)


    def set_token(self, newToken:str):
        '''
        Replace the current token with a new one
        '''
        # set our token
        self.token              = newToken
        self.required_params    = {'access_token': self.token}
        


        

    

    

    
    

