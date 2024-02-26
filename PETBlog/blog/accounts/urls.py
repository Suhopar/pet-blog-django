from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    UserListView,
    PostListView,
    UserRemoveView,
    UserChangeRoleView,
    LikedPostsView,
    ProfileEditView,
)
from django.contrib.auth import views as auth_views

"""

register/, login/, logout/ 
- For registration, authorization.

profile/<int:pk>/ 
- A user's profile page containing information about the user and a list of their publications.

remove-user/<int:pk>/ 
- To remove a user (administrative tool).

change-user-role/<int:pk>/ 
- To change the user/admin role (administrative tool).

users/
- Page with a list of all users (administrative tool).

admin-post-list/
- Page with a list of publications (administrative tool).

"""


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile-edit'),

    path('remove-user/<int:pk>/', UserRemoveView.as_view(), name='remove-user'),
    path('change-user-role/<int:pk>/', UserChangeRoleView.as_view(), name='change-user-role'),

    path('users/', UserListView.as_view(), name='user-list'),
    path('admin-post-list/', PostListView.as_view(), name='admin-post-list'),

    path('user-like-post-list/', LikedPostsView.as_view(), name='user-like-post-list'),



]