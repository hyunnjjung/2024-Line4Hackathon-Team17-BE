from rest_framework import serializers
from .models import Category, PatingPost, PatingParticipation, PatingReport, PatingBlock
from django.contrib.auth import get_user_model

user = get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PatingParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatingParticipation
        fields = ['id', 'user', 'post', 'joined_at']

class PatingPostSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    participants_count = serializers.SerializerMethodField()
    participants = PatingParticipationSerializer(many=True, read_only=True)

    class Meta:
        model = PatingPost
        fields = ['id', 'title', 'content', 'location', 'category', 'time', 'max_participants', 'created_by', 'participants_count', 'participants', 'closed', 'created_at']

    def get_participants_count(self, obj):
        return obj.participants.count()


class PatingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatingReport
        fields = ['id', 'post', 'reported_by']

class PatingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatingBlock
        fields = ['id', 'post', 'blocked_by']
