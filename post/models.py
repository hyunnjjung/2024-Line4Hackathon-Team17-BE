from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model() 

# 공감글 모델
class Post(models.Model):
    title = models.CharField(max_length=50)  # 제목
    content = models.TextField(max_length=100)  # 본문
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    created_at = models.DateTimeField(auto_now_add=True)  # 생성된 날짜, 시간
    support_count = models.PositiveIntegerField(default=0)  # 응원 수
    empathy_count = models.PositiveIntegerField(default=0)  # 공감 수
    congratulations_count = models.PositiveIntegerField(default=0)  # 축하 수
    luck_count = models.PositiveIntegerField(default=0)  # 행운 수

    def __str__(self):
        return self.title

# 공감 모델(응원, 공감, 축하, 행운)
class Reaction(models.Model):
    REACTION_CHOICES = [
        ('support', '응원'),
        ('empathy', '공감'),
        ('congratulations', '축하'),
        ('luck', '행운'),
    ] # 공감 종류 4종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 공감하는 유저
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions') # 공감할 포스트
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES) # 공감 종류

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_reaction')
        ]

# 공감글 신고
class Report(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports') # 신고할 게시물
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 신고하는 유저

# 공감글 차단
class Block(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blocks') # 차단할 게시물
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 차단하는 유저