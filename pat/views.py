from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PatingPost, PatingParticipation, PatingReport, PatingBlock
from .serializers import PatingPostSerializer, PatingParticipationSerializer
from django.shortcuts import get_object_or_404


class PatingPostListCreateView(generics.ListCreateAPIView):
    serializer_class = PatingPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blocked_posts = PatingBlock.objects.filter(blocked_by=self.request.user).values_list('post', flat=True) # 차단한 포스트 들
        reported_posts = PatingReport.objects.filter(reported_by=self.request.user).values_list('post', flat=True) # 신고한 포스트
        
        return PatingPost.objects.exclude(id__in=blocked_posts).exclude(id__in=reported_posts).order_by('-created_at') # 차단하고, 신고한 포스트 제외 모든 포스트 최신순으로 나열(차단한, 신고한 포스트는 안보이게!)

    def perform_create(self, serializer):
        post = serializer.save(created_by=self.request.user) # 요청한 유저가 = 포스트 저자
        PatingParticipation.objects.get_or_create(user=self.request.user, post=post) # 요청한 유저를 유저가 작성한 포스트의 참가자로 등록


class PatingPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = PatingPost.objects.all()
    serializer_class = PatingPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = super().get_object() 
        if PatingBlock.objects.filter(blocked_by=self.request.user, post=post).exists() or PatingReport.objects.filter(reported_by=self.request.user, post=post).exists():
            self.permission_denied(self.request, message="접근 안됨!")
        return post # 요청한 포스트 반환

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by != request.user: # 요청한 유저가 포스트 작성자가 아닐 경우
            return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN) # 삭제 못하게 함
        return super().delete(request, *args, **kwargs) # 요청한 유저가 포스트 작성자이면 삭제
    

class PatingParticipationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = PatingPost.objects.get(id=post_id) # 포스트 불러오기
        if post.closed: # 참여 인원 다 찼을 경우
            return Response({"detail": "이미 마감"}, status=status.HTTP_400_BAD_REQUEST)

        participation, created = PatingParticipation.objects.get_or_create(user=request.user, post=post) # 참여인원 남아있을 경우 요청한 유저를 참가자로 등록

        if not created: # 이미 참여한 경우
            return Response({"detail": "이미 참여 중"}, status=status.HTTP_400_BAD_REQUEST)

        post.check_participants() # 현자 참가인원 파악
        return Response(PatingParticipationSerializer(participation).data, status=status.HTTP_201_CREATED)

class PatingReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(PatingPost, id=post_id)
        if PatingReport.objects.filter(post=post, reported_by=request.user).exists(): # 이미 요청 유저가 신고 했을 경우
            return Response({"detail": "이미 신고함"}, status=status.HTTP_400_BAD_REQUEST)

        report = PatingReport.objects.create(post=post, reported_by=request.user) # 신고
        return Response({"detail": "신고가 완료"}, status=status.HTTP_201_CREATED)

class PatingBlockCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(PatingPost, id=post_id)
        if PatingBlock.objects.filter(post=post, blocked_by=request.user).exists():  # 이미 요청 유저가 차단 했을 경우
            return Response({"detail": "이미 차단함"}, status=status.HTTP_400_BAD_REQUEST)

        block = PatingBlock.objects.create(post=post, blocked_by=request.user) # 차단
        return Response({"detail": "차단이 완료되었습니다."}, status=status.HTTP_201_CREATED)

class MyPatingListView(generics.ListAPIView):
    serializer_class = PatingPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatingPost.objects.filter(created_by=self.request.user).order_by('-created_at') # 내가 작성한 팟팅 글만 최신순으로 나열

class MyPatingPostDeleteView(generics.DestroyAPIView):
    queryset = PatingPost.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.created_by == request.user: # 요청한 유저가 팟팅글 작성자 일때만 포스트 삭제 가능
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

class MyParticipatedPatingListView(generics.ListAPIView):
    serializer_class = PatingPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        participated_posts = PatingParticipation.objects.filter(user=self.request.user).values_list('post', flat=True) # 사용자가 참가하는 팟팅 글 모두 가져오기
    
        return PatingPost.objects.filter(id__in=participated_posts).order_by('-created_at')
