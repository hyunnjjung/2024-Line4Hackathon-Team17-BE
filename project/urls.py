from django.contrib import admin
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/', include('post.urls')), # 공감글
    path('pating/', include('pat.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 토큰 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 갱신
    path('user/', include('user.urls')),
    path('mypage/', include('mypage.urls')),
    path('api/', include('chat.urls')),
    path('api/', include('noti.urls')),
]
