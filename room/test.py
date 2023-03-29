from django.test import TestCase
from django.contrib.auth.models import User
from .models import Room, Message

class MessageModelTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            name='Test Room',
            slug='test-room'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
    
    def test_message_creation(self):
        message = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Test Message'
        )
        self.assertEqual(message.room, self.room)
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.content, 'Test Message')
    
    def test_message_ordering(self):
        message1 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='First Message'
        )
        message2 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Second Message'
        )
        message3 = Message.objects.create(
            room=self.room,
            user=self.user,
            content='Third Message'
        )
        messages = Message.objects.filter(room=self.room)
        self.assertEqual(messages.count(), 3)
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)
        self.assertEqual(messages[2], message3)