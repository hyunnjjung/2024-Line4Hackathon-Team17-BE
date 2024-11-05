from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, InterestViewSet

router = DefaultRouter()
router.register('register', UserViewSet, basename='register')
router.register('interests', InterestViewSet, basename='interests')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
]
