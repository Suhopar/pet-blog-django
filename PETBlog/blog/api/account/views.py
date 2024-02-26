from django.db.models import Count
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from home.models import Category, Post, Comment

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    UserListSerializer,
    AdminPostListSerializer,
)
from api.home.serializers import PostListSerializer, CommentSerializer


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):

    def get(self, request):
        logout(request)
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    def get(self, request, pk):
        user = CustomUser.objects.get(id=pk)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class UserListAPIView(APIView):
    def get(self, request):
        sort_by = request.GET.get('sort_by')
        sort_dir = request.GET.get('sort_dir', 'asc')

        if sort_by:
            user_list = self.sort_users(sort_by, sort_dir)
        else:
            user_list = CustomUser.objects.all()

        serializer = UserListSerializer(user_list, many=True)
        return Response(serializer.data)

    def sort_users(self, sort_by, sort_dir):
        field = sort_by if sort_dir == 'asc' else f'-{sort_by}'

        if sort_by == 'id':
            return CustomUser.objects.all().order_by(field)
        elif sort_by == 'username':
            return CustomUser.objects.all().order_by(field)
        elif sort_by == 'num_posts':
            return CustomUser.objects.annotate(num_posts=Count('post')).order_by(field)
        elif sort_by == 'date_joined':
            return CustomUser.objects.all().order_by(field)
        elif sort_by == 'role':
            return CustomUser.objects.all().order_by(field)
        elif sort_by == 'is_staff':
            return CustomUser.objects.all().order_by(field)
        else:
            return CustomUser.objects.all()


class UserRemoveAPIView(APIView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return CustomUser.objects.filter(pk=pk)

    def delete(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        current_user = self.request.user

        if user and current_user.role == 'admin':
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'User not found or you do not have permission to delete this user.'}, status=status.HTTP_403_FORBIDDEN)


class UserChangeRoleAPIView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)

        if user.role == 'admin':
            user.role = 'user'
        else:
            user.role = 'admin'

        user.save()

        return Response({'message': 'Role changed successfully.'}, status=status.HTTP_200_OK)


class PostListAPIView(APIView):
    def get(self, request):
        sort_by = request.query_params.get('sort_by')
        sort_dir = request.query_params.get('sort_dir', 'asc')

        if sort_by:
            post_list = self.sort_posts(sort_by, sort_dir)
        else:
            post_list = Post.objects.all()

        serializer = AdminPostListSerializer(post_list, many=True)
        print(serializer)
        return Response(serializer.data)

    def sort_posts(self, sort_by, sort_dir):
        field = sort_by if sort_dir == 'asc' else f'-{sort_by}'

        if sort_by == 'date':
            return Post.objects.all().order_by(field)
        elif sort_by == 'title':
            return Post.objects.all().order_by(field)
        elif sort_by == 'author':
            return Post.objects.order_by(field)
        elif sort_by == 'category':
            return Post.objects.order_by('category__title' if sort_dir == 'asc' else '-category__title')
        elif sort_by == 'likes':
            return Post.objects.annotate(like_count=Count('likes__id')).order_by(field, 'title').distinct()
        elif sort_by == 'comment':
            return Post.objects.annotate(comment_count=Count('comment__id')).order_by(field, 'title').distinct()
        elif sort_by == 'hidden':
            return Post.objects.filter(status='hidden')
        elif sort_by == 'published':
            return Post.objects.filter(status='published')
        else:
            return Post.objects.all()