'''
extensions are used to add new functionality to the api wrapper without having to put it in the main codebase.
'''

from facebook_api.facebook_settings import facebook_Config
from facebook_api.request_base import request_base
from facebook_api.extensions.general.me import Me
from facebook_api.extensions.error import RequestError
from facebook_api.extensions.general.accounts import Accounts
from facebook_api.extensions.general.businessAccounts import BusinessAccounts
from facebook_api.extensions.general.media import Posts


class general:
    '''
    general extension for the facebook api wrapper
    '''
    request: request_base = None  # our request base for easy typing

    # init our extension base
    def __init__(self, base: request_base) -> None:
        self.request = base

    def get_me(self):
        '''
        get the current user from facebook that the token is for
        '''
        return self.request.get(self.request.facebook_config.api_version +
                                '/me',
                                object_return_type=Me)

    def get_accounts(self):
        '''
        get the accounts that the user has
        '''
        return self.request.get(self.request.facebook_config.api_version +
                                '/me/accounts',
                                object_return_type=Accounts)

    def get_business_accounts(self):
        '''
        get the business accounts that the user has
        '''
        accounts = self.get_accounts()
        try:
            if (accounts.error):
                return accounts
        except:
            return self.request.get(
                self.request.facebook_config.api_version +
                f'/{accounts.data[0].id}/?fields=instagram_business_account',
                object_return_type=BusinessAccounts)

    def get_posts(self):
        '''
        get the posts from the user
        '''
        account = self.get_business_accounts()
        try:
            if (account.error):
                return account
        except:
            return self.request.get(self.request.facebook_config.api_version +
                                f'/{account.instagram_business_account}/media',
                                object_return_type=Posts)
