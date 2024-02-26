from django.urls import path
from .views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    ProfileAPIView,
    UserListAPIView,
    UserRemoveAPIView,
    UserChangeRoleAPIView,
    PostListAPIView,
)

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='api-register'),
    path('login/', UserLoginAPIView.as_view(), name='api-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='api-logout'),
    path('profile/<int:pk>/', ProfileAPIView.as_view(), name='api-profile'),
    path('user-list/', UserListAPIView.as_view(), name='api-user-list'),
    path('user-remove/<int:pk>/', UserRemoveAPIView.as_view(), name='api-user-remove'),
    path('user-change-role/<int:pk>/', UserChangeRoleAPIView.as_view(), name='api-user-change-role'),
    path('admin-post-list/', PostListAPIView.as_view(), name='api-admin-post-list'),

]