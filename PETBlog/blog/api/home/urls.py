from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostCreateAPIView,
    PostRemoveAPIView,
    PostUpdateAPIView,
    PostStatusChangeAPIView,
    PostLikeAPIView,
    CommentCreateAPIView,
    CommentRemoveAPIView,
    PostSearchAPIView,
    CategoryAPIView,
)

urlpatterns = [
    path('post-list/', PostListAPIView.as_view(), name='api-post-list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='api-post-detail'),
    path('posts/create/', PostCreateAPIView.as_view(), name='api-post-create'),
    path('posts/remove/<int:pk>/', PostRemoveAPIView.as_view(), name='api-post-remove'),
    path('posts/update/<int:pk>/', PostUpdateAPIView.as_view(), name='api-post-update'),
    path('posts/status-change/<int:pk>/', PostStatusChangeAPIView.as_view(), name='api-post-status-change'),
    path('post-like/<int:pk>/', PostLikeAPIView.as_view(), name='api-post-like'),
    path('comment-create/<int:pk>/', CommentCreateAPIView.as_view(), name='api-comment-create'),
    path('comment-remove/<int:pk>/', CommentRemoveAPIView.as_view(), name='api-comment-remove'),
    path('post-search/', PostSearchAPIView.as_view(), name='api-post-search'),
    path('category/<int:pk>/', CategoryAPIView.as_view(), name='api-category'),

]