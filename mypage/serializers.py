from rest_framework import serializers
from django.contrib.auth import get_user_model
from user.models import Interest  # Interest 모델 불러오기

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'gender', 'nickname', 'birth_date', 'address', 'interests']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['nickname', 'interests', 'old_password', 'new_password']

    def validate(self, data):
        # 비밀번호가 변경되는 경우 old_password와 new_password가 모두 존재해야 합니다.
        if 'old_password' in data or 'new_password' in data:
            if not data.get('old_password') or not data.get('new_password'):
                raise serializers.ValidationError("Both old_password and new_password are required to change the password.")
        return data
