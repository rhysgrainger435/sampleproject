from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import SignUpForm



class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword'
        )
    
    def test_profile_creation(self):
        profile = Profile.objects.create(
            user = self.user,
            age = 25,
            name = 'Test Name',
            bio = 'Test Bio'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.age, 25)
        self.assertEqual(profile.name, 'Test Name')
        self.assertEqual(profile.bio, 'Test Bio')

class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.user_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
        self.assertTrue(isinstance(response.context['form'], SignUpForm))

    def test_signup_view_post(self):
        response = self.client.post(self.signup_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('frontpage'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_signup_view_post_invalid_data(self):
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        response = self.client.post(self.signup_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/signup.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())