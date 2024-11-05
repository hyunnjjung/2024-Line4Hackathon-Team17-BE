from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, InterestViewSet

router = DefaultRouter()
router.register('users', UserViewSet,basename='users')
router.register('interests', InterestViewSet,basename='interests')

urlpatterns = [
    path('', include(router.urls)),
]
