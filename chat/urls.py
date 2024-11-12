# chat/urls.py
from django.urls import path
from .views import ChatRoomListView, MessageListView, MessageCreateView, ChatRoomCreateView

urlpatterns = [
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:chat_room_id>/messages/', MessageListView.as_view(), name='chatroom-messages'),
    path('chatrooms/<int:chat_room_id>/messages/send/', MessageCreateView.as_view(), name='send-message'),
    path('chatrooms/create/', ChatRoomCreateView.as_view(), name='create-chatroom'),
]
