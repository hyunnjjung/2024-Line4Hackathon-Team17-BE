from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """모든 알림 조회 (읽지 않은 알림만 조회 가능)"""
        notifications = Notification.objects.filter(receiver=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def create(self, request):
        """알림 생성 (공감 또는 참여)"""
        notification_type = request.data.get("notification_type")
        post_id = request.data.get("post_id")
        post_type = request.data.get("post_type")  # 'post' 또는 'patingpost' 지정
        
        content_model = ContentType.objects.get(model=post_type)
        
        # 알림 생성 로직
        notification = Notification.objects.create(
            receiver=request.user,
            sender=request.user,
            content_type=content_model,
            object_id=post_id,
            notification_type=notification_type,
            post_type=post_type
        )
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def mark_as_read(self, request, pk=None):
        """특정 알림 읽음 처리"""
        notification = get_object_or_404(Notification, id=pk, receiver=request.user)
        notification.is_read = True
        notification.save()
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def unread_count(self, request):
        """읽지 않은 알림 개수 조회"""
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        return Response({"unread_count": unread_count})
