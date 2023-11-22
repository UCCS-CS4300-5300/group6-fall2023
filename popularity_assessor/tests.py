from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from popularity_assessor.models import InstagramAccount
from facebook_api.extensions.general.basicProfileMetrics import BasicProfileMetrics
from facebook_api.extensions.general.postInfo import PostInfo
from facebook_api.extensions.general.media import Posts
from popularity_assessor.views import delete_account, get_posts, mock_user_metrics, mock_posts
from facebook_api.facebook import facebook_API
from facebook_api.facebook_settings import facebook_Config
from django.urls import reverse


def mock_profile_metrics():
    data=         {
            "id": "17841459177727833",
            "username": "podcastclipstoday",
            "media_count": 4,
            "followers_count": 124,
            "follows_count": 68,
            "name": "Podcast clips daily",
            "biography": "\"Motivation and inspiration for personal growth. 🎧 Tune in for podcast clips and daily doses of insight. Join our community! 💪",
            "profile_picture_url": "https://scontent-ord5-2.xx.fbcdn.net/v/t51.2885-15/346926254_192446810356926_4630223781712576112_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=7d201b&_nc_ohc=zSCJrmpVxToAX-ZaD67&_nc_ht=scontent-ord5-2.xx&edm=AL-3X8kEAAAA&oh=00_AfDhhTjGyg62fR0WRyyLa4yXzpvE8wrE4ttbu32dIz6i4Q&oe=655FD404"
        }
    
    return BasicProfileMetrics.from_dict(data)


def mock_posts():
    data = {
                "data": [
                    {
                    "id": "17980895912317725"
                    },
                    {
                    "id": "17988641024004750"
                    },
                    {
                    "id": "17937304004550750"
                    },
                    {
                    "id": "17989257334983575"
                    }
                ],
                "paging": {
                    "cursors": {
                    "before": "QVFIUndweTk5QTFqaVVXTjk2VnZAvN0tZAcmxHd2xNWW5JazJaUHB1NzB0eHRYdzFya01zWFhLTXNNSXpCcVZAQVHctRjNsN01laEYyUDRsempmY2dlcU5RSUxn",
                    "after": "QVFIUkVaSkhFYlZAxRGJndWVQWlFYa3Vla1BVcVlyajBTZA0hfQnMtcEU4R0pJYkEtc016WHRsLUNqcFlHYS11YW9XMTQ4WVRJZAnpKYnJPUXhieFNISDRTaThB"
                    }
                }
            }
    
    return Posts.from_dict(data)

def mock_post_data():
    data =         {
            "like_count": 2,
            "media_url": "https://scontent-iad3-1.cdninstagram.com/o1/v/t16/f1/m82/0C4C916525DF02AE1742724BC26F39B2_video_dashinit.mp4?efg=eyJ2ZW5jb2RlX3RhZyI6InZ0c192b2RfdXJsZ2VuLmNsaXBzLnVua25vd24tQzMuNTc2LmRhc2hfYmFzZWxpbmVfMV92MSJ9&_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_cat=104&vs=544928507820758_700565062&_nc_vs=HBksFQIYT2lnX3hwdl9yZWVsc19wZXJtYW5lbnRfcHJvZC8wQzRDOTE2NTI1REYwMkFFMTc0MjcyNEJDMjZGMzlCMl92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dDYWN0QlFTZUFtRzJXNEdBS0NLOTJKbjRCMDRicV9FQUFBRhUCAsgBACgAGAAbAYgHdXNlX29pbAExFQAAJuTVgdnZxPFAFQIoAkMzLBdANarAgxJumBgSZGFzaF9iYXNlbGluZV8xX3YxEQB1AAA%3D&ccb=9-4&oh=00_AfBJBVE3P_sDc-_aDu1ZEjKQzeFS4rTb8p9niaanOBstFQ&oe=655EC4A3&_nc_sid=1d576d&_nc_rid=deb3ca28cb",
            "permalink": "https://www.instagram.com/reel/CsPyT95AQKc/",
            "timestamp": "2023-05-15T02:15:40+0000",
            "caption": "Surrounding yourself with winners is the key to success 🏆 Follow along as we take inspiration from Kevin Hart and his winning mindset 🤩 Tune in to the Pivot Podcast and Thrive Minds for more motivational videos that will help you reach new heights 🚀 #kevinhart #pivotpodcast #thriveminds #motivationalvideo #fyp",
            "comments_count": 0,
            "media_type": "VIDEO",
            "id": "17989257334983575"
        }
    
    return PostInfo.from_dict(data)


# Test that all the fields appear in the profile view
class ProfileViewGetPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

        ## change the api functions to mock functions
        self.api = facebook_API("test", facebook_Config())

        self.api.general.get_profile_metrics = mock_profile_metrics
        self.api.general.get_posts = mock_posts
        self.api.general.get_post_data = mock_post_data

    def test_profile_view_post_expected_fields(self):
        # Log in test user
        self.client.login(username='testuser', password='testpassword')
        # Retrieve user password page
        response = self.client.get(
            reverse('popularity_assessor:profile', args=['testuser']))
        # Ensure that the response is successfull
        self.assertEqual(response.status_code, 200)
        # # Get expected post data from the get_post function
        # expected_posts = get_posts(None)

        # # Loop each post and assert that each specific field are present
        # for post_data in expected_posts:
        #     self.assertContains(response, post_data['caption'])
        #     self.assertContains(response, post_data['date'])
        #     self.assertContains(response, f'Likes: {post_data["like_count"]}')
        #     self.assertContains(response,
        #                         f'Comments: {post_data["comments_count"]}')


class ProfileViewDeleteAccountTests(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='test_pass')
        self.creds = {'username': 'test', 'password': 'test_pass'}

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

    def tearDown(self):
        pass

    def test_delete_account_button_on_profile_page(self):

        self.client.login(**self.creds)

        response = self.client.get(
            reverse('popularity_assessor:profile',
                    args=(self.creds['username'], )))

        self.assertContains(response, 'Delete Account')

    def test_delete_account_request(self):

        self.client.login(**self.creds)

        response = self.client.post(reverse('popularity_assessor:profile',
                                            args=(self.creds['username'], )),
                                    follow=True)

        self.assertEqual(response.status_code, 200)

        response = self.client.login(**self.creds)
        self.assertEqual(response, False)


class UserAccountTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(self.username, 'test@example.com',
                                             self.password)

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

    def test_registration_view_get(self):
        response = self.client.get(reverse('popularity_assessor:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_valid_post(self):
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'newuser',
                'password1': 'newpassword123',
                'password2': 'newpassword123'
            })
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_registration_invalid_post(self):
        response = self.client.post(
            reverse('popularity_assessor:register'), {
                'username': 'user',
                'password1': 'password',
                'password2': 'notmatching'
            })
        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(response, 'form', 'password2',
                             "The two password fields didn’t match.")

    def test_login_view_get(self):
        response = self.client.get(reverse('popularity_assessor:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_valid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertRedirects(
            response,
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_post(self):
        response = self.client.post(reverse('popularity_assessor:login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' not in self.client.session)
        self.assertFormError(
            response, 'form', None,
            "Please enter a correct username and password. Note that both fields may be case-sensitive."
        )

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('popularity_assessor:logout'))
        self.assertRedirects(response, reverse('popularity_assessor:login'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_view(self):
        # Trying to access the profile page without logging in should redirect to the login page
        response = self.client.get(
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertRedirects(
            response,
            f"{reverse('popularity_assessor:login')}?next={reverse('popularity_assessor:profile', kwargs={'user_name': self.username})}"
        )

        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Now the profile page should be accessible
        response = self.client.get(
            reverse('popularity_assessor:profile',
                    kwargs={'user_name': self.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


# test that if the user passed to delete_account is None, then the function raises a User.DoesNotExist exception
class delete_account_test(TestCase):
    # Make sure that deleting a None user raises a User.DoesNotExist exception
    def test_delete_account_none(self):
        with self.assertRaises(User.DoesNotExist):
            delete_account(None)


# test that if the user is deleted, they don't appear in the database of users

    def test_delete_account_success(self):
        user = User.objects.create_user(username='testuser', password='12345')
        # Call delete_account function to delete user
        delete_account(user)
        # Try retrieving user from databases, should raise User.DoesNotExist exception
        with self.assertRaises(User.DoesNotExist):
            user = User.objects.get(username='testuser')
"""from popularity_assessor.views import get_mock_likes, generate_random_likes, get_posts, get_mock_followers, get_user_metrics
from datetime import datetime, timedelta

class MockDataTests(TestCase):
    def test_get_mock_likes(self):
        # Testing for 5 likes from 1 day ago
        likes = get_mock_likes(5, 1)
        self.assertEqual(len(likes), 5)
        expected_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        for like in likes:
            self.assertEqual(like['date'], expected_date)

    def test_generate_random_likes(self):
        # Testing the generation of random likes
        likes = generate_random_likes()
        self.assertTrue(10 <= len(likes) <= 130)  # Based on the random number generation logic in the function
        today = datetime.now().strftime("%Y-%m-%d")
        for like in likes:
            self.assertIn('date', like)
            self.assertTrue(like['date'] <= today)  # Ensuring the dates are not in the future

    def test_get_posts(self):
        # Testing the creation of mock posts
        posts = get_posts()
        self.assertEqual(len(posts), 5)
        today = datetime.now().strftime("%Y-%m-%d")
        for post in posts:
            self.assertIn('image_path', post)
            self.assertIn('title', post)
            self.assertIn('date', post)
            self.assertIn('likes', post)
            self.assertIn('num_comments', post)
            self.assertEqual(post['date'], '2021-01-0' + str(posts.index(post) + 1))
            self.assertTrue(isinstance(post['likes_today'], int))
            self.assertTrue(post['likes_today'] <= len(post['likes']))  # Ensuring likes_today is not more than total likes

    def test_get_mock_followers(self):
        # Testing the generation of mock followers
        followers = get_mock_followers(10, 2)
        self.assertEqual(len(followers), 10)
        expected_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        for follower in followers:
            self.assertEqual(follower['date'], expected_date)

    def test_get_user_metrics(self):
        # Testing the retrieval of user metrics
        metrics = get_user_metrics()
        self.assertIn('total_followers', metrics)
        self.assertIn('total_following', metrics)
        self.assertIn('total_posts', metrics)
        self.assertIn('followers_today', metrics)
        self.assertIn('followers_one_day_ago', metrics)
        self.assertTrue(isinstance(metrics['total_followers'], int))
        self.assertTrue(isinstance(metrics['total_following'], int))
        self.assertTrue(isinstance(metrics['total_posts'], int))
        self.assertTrue(isinstance(metrics['followers_today'], int))
        self.assertTrue(isinstance(metrics['followers_one_day_ago'], int))"""


class MockMetricsTests(TestCase):
    def test_mock_user_metrics(self):
        metrics = mock_user_metrics()
        self.assertIn('total_posts', metrics)
        self.assertIn('current_followers', metrics)
        self.assertIn('followers_yesterday', metrics)
        self.assertIn('following', metrics)

        # Check the type of values
        self.assertIsInstance(metrics['total_posts'], int)
        self.assertIsInstance(metrics['current_followers'], int)
        self.assertIsInstance(metrics['followers_yesterday'], int)
        self.assertIsInstance(metrics['following'], int)

