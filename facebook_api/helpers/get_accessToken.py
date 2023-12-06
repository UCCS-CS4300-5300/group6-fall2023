from ..extensions.authentication.userAuth import UserAuth   
from ..extensions.error import RequestError                     
from ..extensions.authentication.extendToken import ExtendToken
import requests
import os


class GetAccessToken:
    '''
    get access token class to that is helpers for the facebook api
    '''
    def __init__(self):
        self.client_id = os.getenv("FB_CLIENT_ID")
        self.client_secret = os.getenv("FB_CLIENT_SECRET")

    def user(self, code: str, redirect_url: str) -> UserAuth:
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "code": code,
            "client_id": self.client_id,
            "redirect_uri": "http://" + redirect_url,
            "client_secret": self.client_secret
        }
        resp = requests.get(url, params=params)

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
        if UserAuth != None:
            root = UserAuth.from_dict(resp.json())
            return root

        return resp.json()

    def admin(self) -> UserAuth:
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        resp = requests.get(url, params=params)

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
        if UserAuth != None:
            root = UserAuth.from_dict(resp.json())
            return root

    def debug(self, access_token: str, app_token: str):
        url = "https://graph.facebook.com/debug_token"
        params = {"input_token": access_token, "access_token": app_token}

        resp = requests.get(url, params=params)

        # if we have an error, return the error
        # this will make it easier to use the api since we can just check if the response is an error
        # and if it is, we can just return the error
        # checks to see if we have an error key in the json response
        # or if the status code is greater than 400
        if 'error' in resp:
            print("Error in response")
            error_code = resp['error'].get('code')
            error_subcode = resp['error'].get('error_subcode')

            if error_code == 190:
                if error_subcode == 463:
                    return 'expired'  # Token is expired
                else:
                    return 'invalid'  # Token is invalid for other reasons

        return 'valid'
    
    def extend_token(self, user_access_token: str, app_id: str, app_secret: str):
        url = f"https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={user_access_token}"
        resp = requests.get(url)

        # if we have an error, return the error
        if resp.status_code >= 400 or resp.json().get('error') != None:
            return RequestError.from_dict(resp.json())
        
        # if we have an object return type, we want to return the object
        if ExtendToken != None:
            resp = ExtendToken.from_dict(resp.json())
            return resp