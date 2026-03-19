from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserAuthenticationTest(APITestCase):

    def setUp(self):
        """Set up any initial data for tests."""
        self.registration_url = reverse('user-registration')  # URL for user registration
        self.login_url = reverse('user-login')  # URL for user login
        self.protected_view_url = reverse('protected-view')  # URL for the protected view

        # You can create a test user here, to be used in the tests
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

    def test_user_registration(self):
        """Test user registration view"""
        response = self.client.post(self.registration_url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully!')

    def test_user_login(self):
        """Test login and JWT token issuance"""
        # Register the user first
        self.client.post(self.registration_url, self.user_data, format='json')

        # Log in with the user's credentials
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')

        # Check if access and refresh tokens are returned
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

        # Save the access token for future use
        self.access_token = response.data['access_token']

    def test_access_protected_view(self):
        """Test access to a protected view with a valid token"""
        # Ensure the user is logged in and has a valid access token
        self.test_user_login()  # This will ensure the access_token is set up

        # Use the access token to access the protected view
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        response = self.client.get(self.protected_view_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'This is a protected view!')

    def test_invalid_token_access(self):
        """Test access to a protected view with an invalid token"""
        invalid_token = 'invalidtoken'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + invalid_token)
        response = self.client.get(self.protected_view_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)