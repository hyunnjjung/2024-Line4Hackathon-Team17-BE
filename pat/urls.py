from django.urls import path
from .views import (
    PatingPostListCreateView, PatingPostDetailView,
    PatingParticipationCreateView, PatingReportCreateView,
    PatingBlockCreateView, MyPatingListView, MyPatingPostDeleteView, MyParticipatedPatingListView
)

urlpatterns = [
    path('posts/', PatingPostListCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PatingPostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/join/', PatingParticipationCreateView.as_view(), name='post_join'),
    path('posts/<int:post_id>/report/', PatingReportCreateView.as_view(), name='post_report'),
    path('posts/<int:post_id>/block/', PatingBlockCreateView.as_view(), name='post_block'),
    path('myposts/', MyPatingListView.as_view(), name='my_post_list'),
    path('myposts/<int:pk>/delete/', MyPatingPostDeleteView.as_view(), name='my_post_delete'),
    path('myposts/participated/', MyParticipatedPatingListView.as_view(), name='my_participated_post_list'),
]
