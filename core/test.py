from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

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