from django.contrib import admin
from django.urls import path , include ,re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Your Server Name or Swagger Docs name",
        default_version="Your API version(Custom)",
        description="Your Swagger Docs descriptions",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('community/', include('post.urls')), # 공감글
    path('pating/', include('pat.urls')),
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # 로그인 토큰 발급
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 갱신
    path('user/', include('user.urls')),
    path('mypage/', include('mypage.urls')),
]

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]