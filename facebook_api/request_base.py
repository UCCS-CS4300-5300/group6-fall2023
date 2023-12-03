from facebook_api.facebook_settings import facebook_Config
from facebook_api.extensions.error import RequestError
from facebook_api.utils.constants import BASE_URL
import requests


class request_base:

    # required params for all requests to facebook, this is the access token
    required_params: dict = None

    # store our facebook config so its easier to access
    facebook_config: facebook_Config = None

    def __init__(self, facebook_config: facebook_Config) -> None:
        self.facebook_config = facebook_config
        pass

    def get_access_token(self):
        return self.required_params.get('access_token')


    def get(self, endpoint: str, params: dict = {}, object_return_type: object = None, no_token: bool = False):
        '''
        our get request method to help handle the requests
        this will send a get request to the url with the params added on the end

        endpoint: str - the endpoint to send the request to
        params: dict = {} - the params to add to the end of the url (eg. ?param1=value1&param2=value2)
        object_return_type: object = None - if we want to return an object instead of a dict, we can specify the object type here

        returns: object | dict | RequestError - the response from the request
        object if we have an object_return_type
        dict if we don't have an object_return_type
        RequestError if we have an error
        '''
        # create our url from the base url and the endpoint
        url = BASE_URL + endpoint

        # combine our temp params with the required params and send the response
        params_to_send = {**self.required_params, **params} if not no_token else params
        resp = requests.get(url, params=params_to_send)

        # raise an HTTPError for bad responses
        resp.raise_for_status()

        # if we have an object return type, we want to return the object
        # this will make it easier to use the API since we can get an
        # object back instead of a dict and have to convert it
        if object_return_type is not None:
            root = object_return_type.from_dict(resp.json())
            return root

        return resp.json()
