# noti/urls.py

from django.urls import path
from .views import NotificationViewSet

notification_list = NotificationViewSet.as_view({
    'get': 'list',
})

notification_create = NotificationViewSet.as_view({
    'post': 'create',
})

notification_mark_as_read = NotificationViewSet.as_view({
    'post': 'mark_as_read',
})

notification_unread_count = NotificationViewSet.as_view({
    'get': 'unread_count',
})

urlpatterns = [
    path('noti/', notification_list, name='notification-list'),
    path('noti/create/', notification_create, name='notification-create'),
    path('noti/<int:pk>/read/', notification_mark_as_read, name='notification-mark-as-read'),
    path('noti/unread-count/', notification_unread_count, name='notification-unread-count'),
]
