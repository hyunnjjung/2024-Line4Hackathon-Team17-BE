from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from post.models import Post
from .models import ChatRoom, Message

User = get_user_model()

class ChatAPITestCase(APITestCase):

    def setUp(self):
        # 사용자 생성
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')

        # 게시글 생성
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post",
            author=self.user1
        )

        # 채팅방 생성
        self.chat_room = ChatRoom.objects.create(
            post=self.post,
            user1=self.user1,
            user2=self.user2
        )

        # 메시지 생성
        self.message = Message.objects.create(
            chat_room=self.chat_room,
            sender=self.user1,
            message="Hello, this is a test message"
        )

        # 로그인
        self.client.login(username='user2', password='password123')

    def test_get_chat_room_messages(self):
        url = reverse('chatroom-messages', args=[self.chat_room.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("messages", response.data)
        self.assertEqual(len(response.data["messages"]), 1)
        self.assertEqual(response.data["messages"][0]["message"], "Hello, this is a test message")

    def test_create_chat_room(self):
        url = reverse('create-chatroom')
        data = {"post_id": self.post.id}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["post"], self.post.id)
        self.assertEqual(response.data["user1"], self.user1.id)
        self.assertEqual(response.data["user2"], self.user2.id)
