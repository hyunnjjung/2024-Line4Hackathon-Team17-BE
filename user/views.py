from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, InterestSerializer,UserDetailSerializer
from .models import User, Interest
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({
            "user": RegisterSerializer(result['user']).data,
            "token": result['token']
        }, status=status.HTTP_201_CREATED)
    
     # 특정 사용자의 프로필 정보 조회
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairView.serializer_class
