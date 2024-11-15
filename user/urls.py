from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, InterestViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('register', UserViewSet, basename='register')
router.register('interests', InterestViewSet, basename='interests')

urlpatterns = [
    path('user/', include(router.urls)),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
