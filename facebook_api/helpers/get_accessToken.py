from ..extensions.authentication.userAuth import UserAuth
from ..extensions.error import RequestError
import requests


def get_accessToken(code: str, redirect_url: str) -> UserAuth:


    client_id = "1709283336164932"
    client_secret = "a91ae8bdde78bbed89a013417435a9b7"

    url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {code, client_id, redirect_url, client_secret}
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