from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyPageViewSet

urlpatterns = [
    path('mypage/update_profile/', MyPageViewSet.as_view({'post': 'update_profile'}), name='update_profile'),
    path('mypage/profile/', MyPageViewSet.as_view({'get': 'profile'}), name='profile'),  # 프로필 정보 조회
]
