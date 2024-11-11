from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Report, Block, Reaction
from .serializers import PostSerializer, ReportSerializer
from django.shortcuts import get_object_or_404


# 공감글 전체 조회, 공감글 생성하는 뷰
class CommunityPostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer # postserialzer 이용
    permission_classes = [IsAuthenticated] # 인증된 유저 필요

    def get_queryset(self): # 공감글 반환
        blocked_posts = Block.objects.filter(user=self.request.user).values_list('post', flat=True) # 차단 글 제외 모든 글 반환
        reported_posts = Report.objects.filter(user=self.request.user).values_list('post', flat=True)
        # 차단 및 신고된 글 제외 모든 글 반환
        return Post.objects.exclude(id__in=blocked_posts).exclude(id__in=reported_posts).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context() # request 정보를 serializer에 전달
        context['request'] = self.request
        return context

    def perform_create(self, serializer): # 공감글 작성
        serializer.save(author=self.request.user)  # 요청한 유저 = author


class CommunityPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()  # 모든 post를 가져옴
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'community_post_id'

    def get_object(self): # 공감글 반환
        post = super().get_object()
        # 사용자가 차단한 글하거나 신고한 인지 확인
        if Block.objects.filter(user=self.request.user, post=post).exists() or Report.objects.filter(user=self.request.user, post=post).exists():
            self.permission_denied(
                self.request, message="차단되거나 신고된 글에 접근할 수 없습니다."
            )
        return post

    def delete(self, request, *args, **kwargs): # 공감글 삭제
        post = self.get_object() 
        if post.author == request.user: # 요청한 유저가 글 author일 때만 삭제
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

class CommunityPostReactView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'community_post_id'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        reaction_type = request.data.get('reaction_type')

        if reaction_type not in ['support', 'empathy', 'congratulations', 'luck']:
            return Response({"detail": "올바른 반응 유형을 제공하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 현재 유저의 기존 반응을 가져온다.
        reaction = Reaction.objects.filter(user=user, post=post).first()

        if reaction:
            if reaction.reaction_type == reaction_type:
                # 동일한 반응을 누른 경우: 반응 취소
                reaction.delete()
                decrement_post_reaction_count(post, reaction_type)
                return Response({"detail": f"{reaction_type} 반응이 취소되었습니다."}, status=status.HTTP_200_OK)
            else:
                # 다른 반응으로 변경하는 경우: 기존 반응 취소 후 새로운 반응 추가
                decrement_post_reaction_count(post, reaction.reaction_type)
                reaction.reaction_type = reaction_type
                reaction.save()
                increment_post_reaction_count(post, reaction_type)
                return Response({"detail": f"{reaction_type} 반응으로 변경되었습니다."}, status=status.HTTP_200_OK)
        else:
            # 이전 반응이 없을 경우 새 반응 추가
            Reaction.objects.create(user=user, post=post, reaction_type=reaction_type)
            increment_post_reaction_count(post, reaction_type)
            return Response({"detail": f"{reaction_type} 반응이 추가되었습니다."}, status=status.HTTP_200_OK)

# 공감 수 1 증가
def increment_post_reaction_count(post, reaction_type):
    if reaction_type == 'support':
        post.support_count += 1
    elif reaction_type == 'empathy':
        post.empathy_count += 1
    elif reaction_type == 'congratulations':
        post.congratulations_count += 1
    elif reaction_type == 'luck':
        post.luck_count += 1
    post.save()

# 공감 수 1 감소
def decrement_post_reaction_count(post, reaction_type):
    if reaction_type == 'support' and post.support_count > 0:
        post.support_count -= 1
    elif reaction_type == 'empathy' and post.empathy_count > 0:
        post.empathy_count -= 1
    elif reaction_type == 'congratulations' and post.congratulations_count > 0:
        post.congratulations_count -= 1
    elif reaction_type == 'luck' and post.luck_count > 0:
        post.luck_count -= 1
    post.save()
    

class CommunityPostReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['community_post_id'])
        if Report.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "이미 신고한 글입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        Report.objects.create(user=request.user, post=post)
        return Response({"detail": "신고가 접수되었습니다."}, status=status.HTTP_201_CREATED)


class CommunityPostBlockView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['community_post_id'])
        if Block.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "이미 차단한 글입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        Block.objects.create(user=request.user, post=post)
        return Response({"detail": "차단되었습니다."}, status=status.HTTP_201_CREATED)


class MyCommunityListView(generics.ListAPIView): # 내가 작성한 공감글만 보기
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at') # 최근 생성된 글 순으로 # 요청한 유저가 글의 author인 글을 모두 반환


class MyCommunityPostDeleteView(generics.DestroyAPIView): # 공감글 삭제
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'community_post_id'

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == request.user: # 요청한 유저가 글의 author일때 글 삭제가능
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
