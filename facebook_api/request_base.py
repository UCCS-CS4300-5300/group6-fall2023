from .facebook_settings import facebook_Config
from .extensions.error import RequestError
from .utils.constants import BASE_URL
import requests


class request_base:

    # required params for all requests to facebook, this is the access token
    required_params: dict = None

    # store our facebook config so its easier to access
    facebook_config: facebook_Config = None

    def __init__(self, facebook_config: facebook_Config) -> None:
        self.facebook_config = facebook_config
        pass

    def get(self,
            endpoint: str,
            params: dict = {},
            object_return_type: object = None):
        '''
        our get request method to help handle the requests
        this will send a get request to the url with the params added on the end
        
        endpoint: str - the endpoint to send the request to
        params: dict = {} - the params to add to the end of the url (eg. ?param1=value1&param2=value2)
        object_return_type: object = None - if we want to return an object instead of a dict, we can specify the object type here

        returns: object | dict | RequestError - the response from the request
        object if we have an object_return_type
        dict if we dont have an object_return_type
        RequestError if we have an error
        '''
        # create our url from the base url and the endpoint
        url = BASE_URL + endpoint

        # combine our temp params with the required params and send the response
        # ** unpacks the dict to combine them
        temp_params: dict = {**self.required_params, **params}
        resp = requests.get(url, params=temp_params)

        # if we have an error, return the error
        # this will make it easier to use the api since we can just check if the response is an error
        # and if it is, we can just return the error
        # checks to see if we have an error key in the json response
        # or if the status code is greater than 400
        if resp.status_code >= 400 or resp.json().get('error') != None:
            return RequestError.from_dict(resp.json())

        # if we have an object return type, we want to return the object
        # this will make it easier to use the api sinc we can get an
        # object back instead of a dict and have to convert it
        if object_return_type != None:
            root = object_return_type.from_dict(resp.json())
            return root

        return resp.json()
