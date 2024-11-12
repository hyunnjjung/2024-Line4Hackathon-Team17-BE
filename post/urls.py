from django.urls import path
from .views import (
    CommunityPostListCreateView, CommunityPostDetailView,
    CommunityPostReportView, CommunityPostBlockView,
    MyCommunityListView, MyCommunityPostDeleteView,CommunityPostReactView
)

urlpatterns = [
    path('posts/', CommunityPostListCreateView.as_view(), name='community-post-list-create'),  # 공감글 전체 조회 및 작성
    path('posts/<int:community_post_id>/', CommunityPostDetailView.as_view(), name='community-post-detail-delete'),     # 공감글 조회 및 삭제
    path('posts/<int:community_post_id>/react/', CommunityPostReactView.as_view(), name='community-post-react'),   # 공감글에 공감달기
    path('posts/<int:community_post_id>/report/', CommunityPostReportView.as_view(), name='community-post-report'),     # 공감글 신고
    path('posts/<int:community_post_id>/block/', CommunityPostBlockView.as_view(), name='community-post-block'),    # 공감글 차단
    path('my/community-posts/', MyCommunityListView.as_view(), name='my-community'),     # 내가 쓴 공감글 조회
    path('my/community-posts/<int:community_post_id>/', MyCommunityPostDeleteView.as_view(), name='my-community-post-delete'),     # 내가 쓴 공감글 삭제
]
