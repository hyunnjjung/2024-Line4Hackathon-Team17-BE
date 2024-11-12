from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField()
    post_type = serializers.CharField()  # post_type 필드 추가

    class Meta:
        model = Notification
        fields = ['id', 'receiver', 'sender', 'notification_type', 'created_at', 'is_read', 'post_id', 'post_type']

    def get_post_id(self, obj):
        return obj.object_id
