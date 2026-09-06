from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account
from apps.accounts.serializers import UserSerializer


class AccountModelTests(APITestCase):
    def test_create_user_hashes_password(self):
        user = Account.objects.create_user(
            username='john', email='john@example.com', password='StrongPass123!'
        )
        self.assertNotEqual(user.password, 'StrongPass123!')
        self.assertTrue(user.check_password('StrongPass123!'))


class UserSerializerTests(APITestCase):
    def test_valid_data_creates_user(self):
        serializer = UserSerializer(data={
            'username': 'jane',
            'email': 'jane@example.com',
            'password': 'StrongPass123!',
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, 'jane')
        self.assertTrue(user.check_password('StrongPass123!'))

    def test_weak_password_is_rejected(self):
        serializer = UserSerializer(data={
            'username': 'jane',
            'email': 'jane@example.com',
            'password': '123',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)


class RegisterViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Account.objects.filter(username='newuser').exists())
        self.assertNotIn('password', response.data)

    def test_register_duplicate_username_fails(self):
        Account.objects.create_user(username='dup', email='a@example.com', password='StrongPass123!')
        response = self.client.post(self.url, {
            'username': 'dup',
            'email': 'b@example.com',
            'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        self.user = Account.objects.create_user(
            username='loginuser', email='login@example.com', password='StrongPass123!'
        )

    def test_login_success(self):
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_password_fails(self):
        response = self.client.post(self.url, {
            'username': 'loginuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('logout')
        self.user = Account.objects.create_user(
            username='logoutuser', email='logout@example.com', password='StrongPass123!'
        )

    def test_logout_requires_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout_success_when_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
