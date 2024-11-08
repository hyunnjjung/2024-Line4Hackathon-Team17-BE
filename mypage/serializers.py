from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import Interest  # Interest 모델 불러오기

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'gender', 'nickname', 'birth_date', 'address', 'interests']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'interests']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
