'''
extensions are used to add new functionality to the api wrapper without having to put it in the main codebase.
'''

from ...facebook_settings import facebook_Config
from ...request_base import request_base
from ...extensions.general.me import Me
from ...extensions.error import RequestError
from ...extensions.general.accounts import Accounts
from ...extensions.general.businessAccounts import BusinessAccounts
from ...extensions.general.media import Posts



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
        

    def get_accounts(self) -> Accounts | RequestError:
        '''
        get the accounts that the user has
        '''
        return self.request.get(self.request.facebook_config.api_version + '/me/accounts', object_return_type=Accounts) 
    

    
    def get_business_accounts(self) -> BusinessAccounts | RequestError:
        '''
        get the business accounts that the user has
        '''
        accounts = self.get_accounts()
        if (accounts.error):
            return accounts
        return self.request.get(self.request.facebook_config.api_version + f'/{accounts.data[0].id}/?fields=instagram_business_account', object_return_type=BusinessAccounts)
    
    def get_posts(self) -> Posts | RequestError :
        '''
        get the posts from the user
        '''
        account = self.get_business_accounts()
        if (account.error):
            return account
        return self.request.get(self.request.facebook_config.api_version + f'/{account.instagram_business_account}/media', object_return_type=Posts)
