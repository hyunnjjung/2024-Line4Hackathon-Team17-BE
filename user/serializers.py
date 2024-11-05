from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Interest

User = get_user_model()

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password', 'profile_image', 'is_female', 'nickname', 'birth_date', 'address', 'interests', 'terms_agreement']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        interests = validated_data.pop('interests', [])
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.interests.set(interests)
        return user

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', [])
        instance.interests.set(interests)
        return super().update(instance, validated_data)
