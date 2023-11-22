'''
extensions are used to add new functionality to the api wrapper without having to put it in the main codebase.
'''

from facebook_api.facebook_settings import facebook_Config
from facebook_api.request_base import request_base
from facebook_api.extensions.general.me import Me
from facebook_api.extensions.general.postInfo import PostInfo
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

    # TODO: push this to the DB for less requests
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
        get the posts ids from the user
        TODO: adding abstraction to the posts so we can get the post data
              this will pass a .set_client(self) to the posts so we can call
              the posts.get_info() and it will return the info for that post
        '''
        account = self.get_business_accounts()
        if(type(account) == RequestError):
            return account
        items: Posts = self.request.get(self.request.facebook_config.api_version +
                            f'/{account.instagram_business_account.id}/media',
                            object_return_type=Posts)
        return items
    
    def get_post_data(self, id: int):
        '''
        get the posts information from the user
        Endpoint URL: 17989257334983575?fields=like_count,media_url,permalink,timestamp,caption,comments_count,media_type
        {
            "like_count": 2,
            "media_url": "https://scontent-iad3-1.cdninstagram.com/o1/v/t16/f1/m82/0C4C916525DF02AE1742724BC26F39B2_video_dashinit.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLmNsaXBzLnVua25vd24tQzMuNTc2LmRhc2hfYmFzZWxpbmVfMV92MSJ9&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&vs=544928507820758_700565062&_nc_vs=HBksFQIYT2lnX3hwdl9yZWVsc19wZXJtYW5lbnRfcHJvZC8wQzRDOTE2NTI1REYwMkFFMTc0MjcyNEJDMjZGMzlCMl92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dDYWN0QlFTZUFtRzJXNEdBS0NLOTJKbjRCMDRicV9FQUFBRhUCAsgBACgAGAAbAYgHdXNlX29pbAExFQAAJuTVgdnZxPFAFQIoAkMzLBdANarAgxJumBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1AAA%3D&ccb=9-4&oh=00_AfBJBVE3P_sDc-_aDu1ZEjKQzeFS4rTb8p9niaanOBstFQ&oe=655EC4A3&_nc_sid=1d576d&_nc_rid=deb3ca28cb",
            "permalink": "https://www.instagram.com/reel/CsPyT95AQKc/",
            "timestamp": "2023-05-15T02:15:40+0000",
            "caption": "Surrounding yourself with winners is the key to success 🏆 Follow along as we take inspiration from Kevin Hart and his winning mindset 🤩 Tune in to the Pivot Podcast and Thrive Minds for more motivational videos that will help you reach new heights 🚀 #kevinhart #pivotpodcast #thriveminds #motivationalvideo #fyp",
            "comments_count": 0,
            "media_type": "VIDEO",
            "id": "17989257334983575"
        }
        '''

        data: PostInfo  = self.request.get(self.request.facebook_config.api_version +
                            f'/{id}?fields=like_count,media_url,permalink,timestamp,caption,comments_count,media_type',
                            object_return_type=PostInfo)
        return data
    
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