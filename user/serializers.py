from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Interest

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = User
        fields = [
            'id', 'name', 'username', 'password', 'password_confirmation', 'gender', 
            'nickname', 'birth_date', 'address', 'interests','profile_picture'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        interests = validated_data.pop('interests', [])
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.interests.set(interests)

        # Token 생성
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'token': str(refresh.access_token)
        }

class UserDetailSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True)

    class Meta:
        model = User
        fields = ['gender', 'nickname', 'birth_date', 'interests','profile_picture']


profile_picture= serializers.ImageField(use_url=True, required=False)