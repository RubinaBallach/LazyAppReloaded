from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class UserTestCase(TestCase):
    def setUp(self):
        self.create_user_url = reverse('create-user')

    def test_create_user_success(self):
        payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123'
        }
        # Make POST request to create new user
        response = self.client.post(self.create_user_url, payload)

       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify user exists in the database
        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertTrue(user_exists)

    def test_create_user_invalid_data(self):
        
        payload = {
            'email': 'newuser@example.com',
            'password': 'testpass123'
        }
        # POST request with invalid data
        response = self.client.post(self.create_user_url, payload)

        # Request failed, invalid data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_update_user_success(self):
        # Assuming existence of user setup method
        self.client.login(email='existinguser@example.com', password='password')
        update_url = reverse('update-user', kwargs={'username': 'existinguser'})

        # New data payload for updating the user
        payload = {'email': 'updatedemail@example.com'}
        response = self.client.patch(update_url, payload)

        # Assert the update successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Confirm the user's email was updated
        self.assertEqual(get_user_model().objects.get(username='existinguser').email, payload['email'])


    def test_users_list_authenticated(self):
        # Login as an authenticated user
        self.client.login(email='user@example.com', password='password')
        list_url = reverse('list-users')

        # Attempt to access the user list
        response = self.client.get(list_url)

        #requestsuccessful?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_user_profile_access(self):
        # Login as the user
        self.client.login(email='user@example.com', password='password')
        profile_url = reverse('user-profile')

        # Attempt access to profile
        response = self.client.get(profile_url)

        # profile is accessible?
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_inactive_user(self):
        # Setup an inactive user
        user = get_user_model().objects.create_user(email="inactive@example.com", username='inactiveuser', password='password123', is_active=False)
        login_url = reverse('login')

        # Try login with inactive user
        response = self.client.post(login_url, {'email': 'inactive@example.com', 'password': 'password123'})

        #login is unsuccessful?
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
