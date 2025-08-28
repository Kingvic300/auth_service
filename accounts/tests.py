from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.cache import cache
from .models import User
from .utils import generate_reset_token, store_reset_token, verify_reset_token


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.registration_url = reverse('user-register')
        self.user_data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())

    def test_user_registration_password_mismatch(self):
        self.user_data['password_confirm'] = 'differentpass'
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.registration_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('user-login')
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            password='testpass123'
        )

    def test_user_login_success(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetTestCase(APITestCase):
    def setUp(self):
        self.forgot_password_url = reverse('forgot-password')
        self.reset_password_url = reverse('reset-password')
        self.user = User.objects.create_user(
            email='test@example.com',
            full_name='Test User',
            password='oldpass123'
        )

    def test_forgot_password_success(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_invalid_email(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_password_success(self):
        token = generate_reset_token()
        store_reset_token('test@example.com', token)

        data = {
            'token': token,
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password_invalid_token(self):
        data = {
            'token': 'invalid_token',
            'new_password': 'newpass123',
            'confirm_password': 'newpass123'
        }
        response = self.client.post(self.reset_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UtilsTestCase(TestCase):
    def test_generate_reset_token(self):
        token = generate_reset_token()
        self.assertEqual(len(token), 32)
        self.assertTrue(token.isalnum())

    def test_store_and_verify_reset_token(self):
        email = 'test@example.com'
        token = generate_reset_token()

        # Store token
        result = store_reset_token(email, token, expiry_minutes=1)
        self.assertTrue(result)

        # Verify token
        retrieved_email = verify_reset_token(token)
        self.assertEqual(retrieved_email, email)

        # Token should be deleted after verification
        retrieved_email_again = verify_reset_token(token)
        self.assertIsNone(retrieved_email_again)

    def tearDown(self):
        cache.clear()