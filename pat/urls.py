from django.urls import path
from .views import (
    PatingPostListCreateView, PatingPostDetailView,
    PatingParticipationCreateView, PatingReportCreateView,
    PatingBlockCreateView, MyPatingListView, MyPatingPostDeleteView, MyParticipatedPatingListView
)

urlpatterns = [
    path('pating/posts/', PatingPostListCreateView.as_view(), name='post_list_create'),
    path('pating/posts/<int:pk>/', PatingPostDetailView.as_view(), name='post_detail'),
    path('pating/posts/<int:post_id>/join/', PatingParticipationCreateView.as_view(), name='post_join'),
    path('pating/posts/<int:post_id>/report/', PatingReportCreateView.as_view(), name='post_report'),
    path('pating/posts/<int:post_id>/block/', PatingBlockCreateView.as_view(), name='post_block'),
    path('pating/myposts/', MyPatingListView.as_view(), name='my_post_list'),
    path('pating/myposts/<int:pk>/delete/', MyPatingPostDeleteView.as_view(), name='my_post_delete'),
    path('pating/myposts/participated/', MyParticipatedPatingListView.as_view(), name='my_participated_post_list'),
]
