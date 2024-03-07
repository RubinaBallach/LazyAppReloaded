from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class FlatApplicationsTests(APITestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_create_lazy_renter_profile(self):
        url = reverse('flat_applications:lazyrenter-profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_landlord(self):
        url = reverse('flat_applications:landlord')
        data = {
            'name': 'Jane Doe',
            'contact_info': 'Contact info here',
            # Include other fields as per model
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_flat_application(self):
        url = reverse('flat_applications:flat-application')
        data = {
            #'flat_ad_link' to be included 
            'flat_ad_link': 'http://example.com/flat',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_lazy_renter_profile(self):
        #create a renter profile here or adjust the URL if it's dynamic?
        url = reverse('flat_applications:lazyrenter-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Further assertions can be added to validate the response data
