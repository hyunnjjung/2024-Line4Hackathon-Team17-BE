from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, InterestSerializer
from .models import User, Interest

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

class InterestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairView.serializer_class
