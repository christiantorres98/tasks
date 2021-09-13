from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from users.serializers import UserModelSerializer

LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')


class UserTestCase(TestCase):
    """Test the users API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user',
            email='test_user@gmail.com',
            password='test123**.'
        )

    def test_failed_login(self):
        payload = {
            'username': 'test_user',
            'password': 'wrong_password'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_login(self):
        payload = {
            'username': 'test_user',
            'password': 'test123**.'
        }
        res = self.client.post(LOGIN_URL, payload)
        serializer = UserModelSerializer(self.user)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['user'], serializer.data)
        self.assertIn('token', res.data)
        token = Token.objects.filter(user=self.user)
        self.assertTrue(token)

    def test_failed_logout(self):
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        payload = {
            'username': 'test_user',
            'password': 'test123**.'
        }
        res = self.client.post(LOGIN_URL, payload)
        self.client.force_authenticate(user=self.user, token=res.data['token'])
        res = self.client.post(LOGOUT_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_signup_failed_by_missing_data(self):
        payload = {
            'username': 'user_signup_test',
            'password': 'test123**.',
            'password_confirmation': 'test123**.'
        }
        res = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_failed_by_duplicated_username(self):
        payload = {
            'username': 'test_user',
            'first_name': 'user',
            'last_name': 'test',
            'email': 'user_signup_test@test.com',
            'password': 'test123**.',
            'password_confirmation': 'test123**.'
        }
        res = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data)

    def test_signup_failed_by_duplicated_email(self):
        payload = {
            'username': 'user_signup_test',
            'first_name': 'user',
            'last_name': 'test',
            'email': 'test_user@gmail.com',
            'password': 'test123**.',
            'password_confirmation': 'test123**.'
        }
        res = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data)

    def test_signup_failed_by_mismatch_passwords(self):
        payload = {
            'username': 'user_signup_test',
            'first_name': 'user',
            'last_name': 'test',
            'email': 'user_signup_test@test.com',
            'password': 'test123**.',
            'password_confirmation': 'wrong_confirmation'
        }
        res = self.client.post(SIGNUP_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data)

    def test_successful_signup(self):
        payload = {
            'username': 'user_signup_test',
            'first_name': 'user',
            'last_name': 'test',
            'email': 'user_signup_test@test.com',
            'password': 'test123**.',
            'password_confirmation': 'test123**.'
        }
        res = self.client.post(SIGNUP_URL, payload)
        user = User.objects.get(username='user_signup_test')
        serializer = UserModelSerializer(user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
