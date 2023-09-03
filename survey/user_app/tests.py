from django.test import TestCase
from .models import User
from django.urls import reverse

class UserTestCase(TestCase):
    
    def setUp(self) -> None:
        User.objects.create_user(username='test', password='password')
        
    def test_user_login(self):
        
        data = {
            'username':'test',
            'password':'password'
        }
        
        response = self.client.post(reverse('login'), data)
        self.assertTrue(response.status_code, 200)