from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyPageViewSet

router = DefaultRouter()
router.register('mypage', MyPageViewSet, basename='mypage')

urlpatterns = [
    path('', include(router.urls)),
]
