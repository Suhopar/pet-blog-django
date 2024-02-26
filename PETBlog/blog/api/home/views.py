from django.urls import reverse
from rest_framework import generics
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from home.models import Category, Post, Comment

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    PostStatusChangeSerializer,
    PostLikeSerializer,
    CommentCreateSerializer,
    PostSearchSerializer,
    PostCategorySerializer,
)


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostDetailAPIView(APIView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        comment_data = request.data
        comment_data['post'] = pk
        serializer = CommentSerializer(data=comment_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.all()


class PostRemoveAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        return Post.objects.all()

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        user = self.request.user

        if post.author == user or user.role == 'admin':
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PostUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostUpdateSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class PostStatusChangeAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostStatusChangeSerializer

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user

        if user.role == 'admin':
            post.status = 'hidden' if post.status == 'published' else 'published'
            post.save()

            serializer = self.get_serializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PostLikeAPIView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        likes_count = post.likes.count()

        serializer = PostLikeSerializer(data={'liked': liked, 'likes_count': likes_count})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        serializer.save(post=post, author=self.request.user, status='published')

    def get_queryset(self):
        return Comment.objects.all()


class CommentRemoveAPIView(generics.DestroyAPIView):
    def get_queryset(self):
        return Comment.objects.all()

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        user = self.request.user

        if comment.author == user or user.role == 'admin':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class PostSearchAPIView(generics.ListAPIView):
    serializer_class = PostSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', 'lo')
        return Post.objects.filter(title__icontains=query)


class CategoryAPIView(generics.ListAPIView):
    serializer_class = PostCategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Post.objects.filter(category_id=category_id)