from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.core import mail

class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="user@example.com", username='testuser', password='password123')
        self.login_url = reverse('login')  
    # Login view and url configured? of course fucking not

    def test_valid_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password123'})
        self.assertTrue(response.context['user'].is_authenticated)
        pass
        #verify login

    def test_invalid_password_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertFalse(response.context['user'].is_authenticated) 
    #verify invalid pass

    def test_blank_fields_login(self):
        response = self.client.post(self.login_url, {'username': '', 'password': ''})
        self.assertIn('This field is required.', response.context['form'].errors['username'])
        self.assertIn('This field is required.', response.context['form'].errors['password'])
    #verify if blank field 

    def test_forgot_password(self):
        response = self.client.post(reverse('password_reset'), {'email': 'self.user.email'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('password reset', mail.outbox[0].subject)
    #verify "forgot password" function

    def test_invalid_login_message(self):
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertIn('Invalid credentials', response.content.decode())
    #verify message for invalid login