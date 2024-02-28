from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



User = get_user_model()

class UserAPITestCase(APITestCase):
    
    def setUp(self):
        #create user for auth test
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user_token = Token.objects.create(user=self.test_user)
        self.create_user_url = reverse('create-user')
        self.login_url = reverse('login')
        self.list_users_url = reverse('list-users')
        self.user_profile_url = reverse('user-profile', kwargs={'user_id': self.test_user.user_id})
        self.update_user_url = reverse('update-user', kwargs={'user_id': self.test_user.user_id})


    def test_create_user_success(self):
        
        payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'first_name':'testname1',
            'last_name':'testname',
        }
        
        response = self.client.post(self.create_user_url, payload, format='json')
        print (response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_data(self):
        
        payload = {
            'email': 'newuser@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.create_user_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

    def test_update_user_success(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        payload = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'testpass123',
            'first_name':'testname1',
            'last_name':'testname',
        }

        
        
        
        payload ['first_name'] = 'Alex'
        response = self.client.put(self.update_user_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, 'newuser@example.com')
        
       
    def test_users_list_authenticated(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = self.client.get(self.list_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_user_profile_access(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_login_inactive_user(self):
        # create inactive user
        inactive_user = User.objects.create_user('inactiveuser', 'inactive@example.com', 'password123', is_active=False)
        inactive_user_token = Token.objects.create(user=inactive_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + inactive_user_token.key)
        response = self.client.post(self.login_url, {'username': 'inactiveuser', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
