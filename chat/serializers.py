# chat/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat_room", "sender", "message", "created_at", "is_read"]

class ChatRoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_message_time = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ["id", "post", "other_user", "last_message", "last_message_time", "unread_count"]

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return last_message.message if last_message else None

    def get_last_message_time(self, obj):
        last_message = obj.messages.last()
        return last_message.created_at if last_message else None

    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.get_unread_count(user)

    def get_other_user(self, obj):
        user = self.context['request'].user
        other_user = obj.user1 if obj.user2 == user else obj.user2
        return {"id": other_user.id, "username": other_user.username}
