'''
extensions are used to add new functionality to the api wrapper without having to put it in the main codebase.
'''

from datetime import datetime, timedelta
import json
import requests
from facebook_api.request_base import request_base
from facebook_api.extensions.general.me import Me
from facebook_api.extensions.general.postInfo import PostInfo
from facebook_api.extensions.error import RequestError
from facebook_api.extensions.general.accounts import Accounts
from facebook_api.extensions.general.businessAccounts import BusinessAccounts
from facebook_api.extensions.general.media import Posts
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics
from facebook_api.extensions.profile.profileFollows import ProfileFollows
from facebook_api.extensions.profile.profileViews import ProfileViews


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

        # Check if accounts is None
        if accounts is None:
            return None  # or raise an exception or handle accordingly

        # Check for the presence of the 'error' attribute
        if hasattr(accounts, 'error') and accounts.error:
            return accounts
        else:
            account_id = accounts.data[0].id
            endpoint = (
                f'{self.request.facebook_config.api_version}/{account_id}/?fields=instagram_business_account'
            )

            return self.request.get(endpoint,
                                    object_return_type=BusinessAccounts)

    def get_posts(self):
        '''
        get the posts ids from the user
        TODO: adding abstraction to the posts so we can get the post data
            this will pass a .set_client(self) to the posts so we can call
            the posts.get_info() and it will return the info for that post
        '''
        account = self.get_business_accounts()
        if isinstance(account, RequestError):
            return account

        # Use the f-string for better readability
        endpoint = f'{self.request.facebook_config.api_version}/{account.instagram_business_account.id}/media'

        items = self.request.get(endpoint, object_return_type=Posts)
        return items

    def get_post_data(self, post_id: int):
        '''
        get the posts information from the user
        Endpoint URL: 17989257334983575?fields=like_count,media_url,permalink,timestamp,caption,comments_count,media_type
        '''
        endpoint = f'{self.request.facebook_config.api_version}/{post_id}?fields=like_count,media_url,permalink,timestamp,caption,comments_count,media_type'

        data = self.request.get(endpoint, object_return_type=PostInfo)
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

        # Check if account is None
        if account is None:
            return None  # or raise an exception or handle accordingly

        # Check for the presence of the 'error' attribute
        if hasattr(account, 'error') and account.error:
            return account
        else:
            endpoint = f'{self.request.facebook_config.api_version}/{account.instagram_business_account.id}?fields=id,username,media_count,followers_count,follows_count,name,biography,profile_picture_url'

            data = self.request.get(endpoint,
                                    object_return_type=BasicProfileMetrics)
            return data

    def calculate_date_range(self):
        # Get the current date and time
        current_datetime = datetime.now()

        # Create a timedelta of 7 days
        seven_days_delta = timedelta(days=7)

        # Calculate the date for 7 days ago
        seven_days_ago_datetime = current_datetime - seven_days_delta

        # Format the dates as strings
        current_datetime_string = current_datetime.strftime('%Y-%m-%d')
        seven_days_ago_date_string = seven_days_ago_datetime.strftime(
            '%Y-%m-%d')

        return seven_days_ago_date_string, current_datetime_string

    def get_profile_follows(self):
        account = self.get_business_accounts()

        # Check if account is None
        if account is None:
            return None  # or raise an exception or handle accordingly

        # Check for the presence of the 'error' attribute
        if hasattr(account, 'error') and account.error:
            return account
        else:
            # Calculate the date range
            start_date, end_date = self.calculate_date_range()

            endpoint = (
                f'{self.request.facebook_config.api_version}/'
                f'{account.instagram_business_account.id}/insights/follower_count?'
                f'since={start_date}&until={end_date}&period=day')

            data = self.request.get(endpoint,
                                    object_return_type=ProfileFollows)
            return data

    def get_profile_views(self):
        account = self.get_business_accounts()

        # Check if account is None
        if account is None:
            return None  # or raise an exception or handle accordingly

        # Check for the presence of the 'error' attribute
        if hasattr(account, 'error') and account.error:
            return account
        else:
            # Calculate the date range
            start_date, end_date = self.calculate_date_range()

            endpoint = (
                f'{self.request.facebook_config.api_version}/'
                f'{account.instagram_business_account.id}/insights/profile_views?'
                f'since={start_date}&until={end_date}&period=day')

            data: ProfileViews = self.request.get(
                endpoint, object_return_type=ProfileViews)
            return data

    def get_batch_post_data(self) -> 'list[PostInfo]':
        posts = self.get_posts()
        post_ids = [posts.data[i].id for i in range(len(posts.data))]

        batch_request = [{
            'method':
            'GET',
            'relative_url':
            f'{post_id}?fields=like_count,media_url,permalink,timestamp,caption,comments_count,media_type'
        } for post_id in post_ids]

        params = {
            'access_token': self.request.get_access_token(),
            'batch': batch_request,
        }

        try:
            response = requests.post('https://graph.facebook.com', json=params)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()

            # Process the response
            data = [
                json.loads(d['body']) for d in data
                if json.loads(d['body']).get('media_type') == 'IMAGE'
            ]

            posts_data = [
                PostInfo.from_dict({
                    **post, 'timestamp':
                    post.get('timestamp', '').split('T')[0]
                }) for post in data
            ]

            for post in posts_data:
                post.caption = post.caption.split()

            return posts_data

        except requests.exceptions.RequestException as e:
            # Handle the error (e.g., log it, return a default response, etc.)
            return f"Error fetching batch post data: {str(e)}"
