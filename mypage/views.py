from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password

from .serializers import *

User = get_user_model()

class MyPageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """내 프로필 정보 보이기"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_potting(self, request):
        """내가 만든 팟팅 모아보기 - RD 기능 (placeholder)"""
        return Response({"message": "내가 만든 팟팅 리스트"})

    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """내가 쓴 공감 글 모아보기 - RD 기능 (placeholder)"""
        return Response({"message": "내가 쓴 공감 글 리스트"})

    @action(detail=False, methods=['get'])
    def participated_potting(self, request):
        """팟팅 참여 내역 모아보기 (placeholder)"""
        return Response({"message": "팟팅 참여 내역 리스트"})

    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        """정보수정 - 닉네임, 관심사, 비밀번호 변경"""
        user = request.user

        # 닉네임 및 관심사 업데이트
        nickname = request.data.get('nickname')
        interests = request.data.get('interests')
        if nickname:
            user.nickname = nickname
        if interests is not None:
            user.interests.set(interests)

        # 비밀번호 업데이트
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password and new_password:
            if not check_password(old_password, user.password):
                return Response({"old_password": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)

        user.save()
        return Response({"message": "Profile updated successfully"})
