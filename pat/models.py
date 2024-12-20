from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model

class Category(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class PatingPost(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    location = models.CharField(max_length=100)
    time = models.CharField(max_length=20)
    max_participants = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    def check_participants(self):
        if self.participants.count() >= self.max_participants:
            self.closed = True
            self.save()

class PatingParticipation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    post = models.ForeignKey(PatingPost, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class PatingReport(models.Model):
    post = models.ForeignKey(PatingPost, on_delete=models.CASCADE, related_name='reports') # 신고할 게시물
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 신고하는 유저

class PatingBlock(models.Model):
    post = models.ForeignKey(PatingPost, on_delete=models.CASCADE, related_name='blocks') # 차단할 게시물
    blocked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 차단하는 유저