from django.test import TestCase, LiveServerTestCase
from django.contrib.auth.models import User
from popularity_assessor.models import InstagramAccount
from popularity_assessor.views import delete_account, get_posts, mock_user_metrics, mock_posts, get_followers
from django.urls import reverse
from datetime import datetime, timedelta

# Test the get_follower function
class GetFollowersTests(TestCase):
    def test_get_followers(self):
      # Call function to get data
      dates, followers = get_followers()
      
      # Assert based on the expected structure of the data
      self.assertEqual(len(dates), 7)
      self.assertEqual(len(followers), 7)

      for data in dates:
        self.assertTrue(isinstance(data, str))
        self.assertTrue(datetime.strptime(data, "%Y-%m-%d"))

      # Check type of each follower count
      for count in followers:
        self.assertTrue(isinstance(count, int))
        
# Test that all the fields appear in the profile view
class ProfileViewGetPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

        self.ig = InstagramAccount(user=self.user, token='test')
        self.ig.save()

    def test_profile_view_post_expected_fields(self):
        # Log in test user
        self.client.login(username='testuser', password='testpassword')
        # Retrieve user password page
        response = self.client.get(
            reverse('popularity_assessor:profile', args=['testuser']))
        # Ensure that the response is successfull
        self.assertEqual(response.status_code, 200)
        # Get expected post data from the get_post function
        expected_posts = get_posts(None)

        # Loop each post and assert that each specific field are present
        for post_data in expected_posts:
            self.assertContains(response, post_data['title'])
            self.assertContains(response, post_data['date'])
            self.assertContains(response, f'Likes: {post_data["likes"]}')
            self.assertContains(response,
                                f'Comments: {post_data["num_comments"]}')


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


class MockPostsTests(TestCase):
    def test_mock_posts(self):
        posts = mock_posts()

        # Check if posts is a list
        self.assertIsInstance(posts, list)

        # Check the structure of each post
        for post in posts:
            self.assertIn('image_path', post)
            self.assertIn('title', post)
            self.assertIn('date', post)
            self.assertIn('likes', post)
            self.assertIn('num_comments', post)

            # Check the type of each attribute
            self.assertIsInstance(post['title'], str)
            self.assertIsInstance(post['date'], str)
            self.assertIsInstance(post['likes'], list)
            self.assertIsInstance(post['num_comments'], int)

            # Check the structure of each like
            for like in post['likes']:
                self.assertIn('timestamp', like)
                self.assertIsInstance(like['timestamp'], str)
