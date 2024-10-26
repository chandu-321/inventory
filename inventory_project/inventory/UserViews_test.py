# inventory/tests.py
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

class UserAuthTests(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.username = "testuser"
        self.password = "securepassword123"
        self.register_url = reverse('register')  # Adjust to the actual URL name
        self.login_url = reverse('login')  # Adjust to the actual URL name

    def test_user_registration(self):
        response = self.client.post(self.register_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], self.username)

    def test_registration_existing_user(self):
        self.client.post(self.register_url, {
            'username': self.username,
            'password': self.password
        })
        response = self.client.post(self.register_url, {
            'username': self.username,
            'password': "newpassword456"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "User already exists.")

    def test_user_login_successful(self):
        
        self.User.objects.create_user(username=self.username, password=self.password)
        
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_user_login_invalid_credentials(self):
        self.User.objects.create_user(username=self.username, password=self.password)
        
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': "wrongpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials.")
