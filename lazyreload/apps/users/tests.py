from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token 
from faker import Faker



User = get_user_model()

class UserAPITestCase(APITestCase):
    
    def setUp(self):
        self.fake = Faker()
        
                
        #create user for auth test and faker shenaningans
        self.test_user = User.objects.create_user(
            username=self.fake.user_name(),
            email=self.fake.email(),
            password='testpassword'
        )
        
        self.test_user.is_staff = True #so you don't get 403'd on 2 tests (delete and update)
        self.test_user.save()
        
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword') #hardcoded stuff
        self.test_user_token = Token.objects.create(user=self.test_user)
        
        self.test_admin_user = User.objects.create_superuser('adminuser', 'admin@example.com', 'adminpassword')
        self.test_admin_token = Token.objects.create(user=self.test_admin_user)
        
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
        
       
    def test_users_list_authenticated(self): #assure that auth is admin, needs rewrite as admin_user, otherwise permission and access control test fails
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_admin_token.key)
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

    def test_delete_user(self):
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.test_user_token.key)
        delete_url = reverse('delete-user', kwargs={'user_id': self.test_user.user_id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.test_user.user_id)
    
    def test_permission_and_access_control(self): #fails, need to check user-list('list-users' in this case). Permission issue, because a reg user is not supposed to access the list
        regular_user = User.objects.create_user(username=self.fake.user_name(), email=self.fake.email(), password='password123')
        regular_user_token = Token.objects.create(user=regular_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + regular_user_token.key)
        response = self.client.get(reverse('list-users'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg="Regular user should not access user list")
        
    def test_login_with_wrong_password(self):
        user = User.objects.create(username=self.fake.user_name(), email=self.fake.email(), password='correctpassword')
        payload = {'username': user.username, 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), payload, format='json')
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Invalid credentials')
                                                