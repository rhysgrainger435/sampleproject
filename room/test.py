from django.test import TestCase
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User
from .models import Room, Message
from .consumers import Room, Message, ChatConsumer

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

class ChatConsumerTestCase(TestCase):

    async def connect(self, room_name):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), f'/ws/chat/{room_name}/')
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def disconnect(self, communicator):
        await communicator.disconnect()

    async def send_message(self, communicator, message, username, room):
        await communicator.send_json_to({
            'message': message,
            'username': username,
            'room': room,
        })

    async def receive_message(self, communicator):
        message = await communicator.receive_json_from()
        self.assertIn('message', message)
        self.assertIn('username', message)
        return message

    async def test_chat_consumer(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        room = Room.objects.create(name='testroom', slug='testroom')
        message = 'Test message'
        communicator1 = await self.connect(room.slug)
        communicator2 = await self.connect(room.slug)

        
        await self.send_message(communicator1, message, user.username, room.slug)
        response = await self.receive_message(communicator1)
        self.assertEqual(response['message'], message)

        
        await self.send_message(communicator2, message, user.username, room.slug)
        response = await self.receive_message(communicator1)
        self.assertEqual(response['message'], message)
        response = await self.receive_message(communicator2)
        self.assertEqual(response['message'], message)

        
        saved_message = Message.objects.last()
        self.assertEqual(saved_message.content, message)
        self.assertEqual(saved_message.user, user)
        self.assertEqual(saved_message.room, room)

        await self.disconnect(communicator1)
        await self.disconnect(communicator2)