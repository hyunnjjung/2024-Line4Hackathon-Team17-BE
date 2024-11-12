from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('support', '격려'),
        ('empathy', '공감'),
        ('congratulations', '축하'),
        ('luck', '행운'),
        ('join', '참여')
    ]
    
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # 알림을 받는 사용자
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_notifications")  # 알림을 보낸 사용자

    # 관련된 게시물
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Post나 PatingPost를 참조
    object_id = models.PositiveIntegerField()  # Post 또는 PatingPost의 ID
    content_object = GenericForeignKey('content_type', 'object_id')  # 실제 객체에 대한 참조

    post_type = models.CharField(max_length=50)  # 게시물 유형 ('post' 또는 'patingpost')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # 읽음 여부 표시

    def __str__(self):
        return f"{self.receiver}에게 {self.notification_type} 알림"
