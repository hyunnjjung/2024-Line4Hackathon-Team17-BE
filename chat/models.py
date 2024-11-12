# chat/models.py
from django.db import models
from django.conf import settings
from post.models import Post

class ChatRoom(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="chat_rooms")
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1_rooms")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user2_rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
