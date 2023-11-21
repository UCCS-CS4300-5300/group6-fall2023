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
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics


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
    def get_profile_metrics(self):
        '''
        Gets basic metrics for now
        Endpoint URL: 17841459177727833?fields=id,username,media_count,followers_count,follows_count,name,biography,
        example return:
        {
            "id": "17841459177727833",
            "username": "podcastclipstoday",
            "media_count": 4,
            "followers_count": 124,
            "follows_count": 68,
            "name": "Podcast clips daily",
            "biography": "\"Motivation and inspiration for personal growth. 🎧 Tune in for podcast clips and daily doses of insight. Join our community! 💪",
            "profile_picture_url": "https://scontent-ord5-2.xx.fbcdn.net/v/t51.2885-15/346926254_192446810356926_4630223781712576112_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=7d201b&_nc_ohc=zSCJrmpVxToAX-ZaD67&_nc_ht=scontent-ord5-2.xx&edm=AL-3X8kEAAAA&oh=00_AfDhhTjGyg62fR0WRyyLa4yXzpvE8wrE4ttbu32dIz6i4Q&oe=655FD404"
        }
        '''
        account = self.get_business_accounts()
        try:
            if (account.error):
                return account
        except:
            return self.request.get(self.request.facebook_config.api_version +
                                f'/{account.instagram_business_account.id}?fields=id,username,media_count,followers_count,follows_count,name,biography,profile_picture_url', object_return_type=BasicProfileMetrics)