# chat/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from post.models import Post
from django.db import models


class ChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(models.Q(user1=user) | models.Q(user2=user))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_room_id = self.kwargs["chat_room_id"]
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        return chat_room.messages.all()

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chat_room_id = self.kwargs["chat_room_id"]
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        message = request.data.get("message")

        new_message = Message.objects.create(
            chat_room=chat_room, sender=request.user, message=message
        )
        chat_room.messages.add(new_message)
        return Response(MessageSerializer(new_message).data, status=status.HTTP_201_CREATED)

class ChatRoomCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get("post_id")
        post = get_object_or_404(Post, id=post_id)
        user1 = post.author
        user2 = request.user

        # 채팅방이 이미 존재하는지 확인
        chat_room, created = ChatRoom.objects.get_or_create(
            post=post, user1=user1, user2=user2
        )

        if created:
            # 새로운 채팅방이 생성된 경우
            return Response(ChatRoomSerializer(chat_room, context={"request": request}).data, status=status.HTTP_201_CREATED)
        else:
            # 기존 채팅방이 이미 있는 경우 해당 채팅방 ID를 반환
            return Response({
                "detail": "Chat room already exists.",
                "chat_room_id": chat_room.id
            }, status=status.HTTP_200_OK)