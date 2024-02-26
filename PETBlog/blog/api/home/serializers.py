from rest_framework import serializers
from home.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    """

    Serializer for representing Category model.

    Fields:
    - id
    - title

    """
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """

    Serializer for representing Comment model.

    Fields:
    - id
    - post
    - author
    - content
    - date
    - status

    """
    class Meta:
        model = Comment
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    """

    Serializer for representing a list of Post models.

    Fields:
    - id
    - title
    - content
    - image
    - date
    - status
    - category
    - author
    - likes

    """
    class Meta:
        model = Post
        fields = '__all__'


class PostDetailSerializer(serializers.ModelSerializer):
    """

    Serializer for representing a detailed view of a Post model.

    Fields:
    - id
    - title
    - content
    - image
    - date
    - status
    - category
    - author
    - likes
    - comments

    Methods:
    - get_comments

    """
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'date', 'status', 'category', 'author', 'likes', 'comments']

    def get_comments(self, obj):
        request = self.context.get('request')
        comments = Comment.objects.filter(post=obj)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return serializer.data


class PostCreateSerializer(serializers.ModelSerializer):
    """

    Serializer for creating a new post.

    Fields:
    - title
    - content
    - category
    - image

    Methods:
    - create

    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

    def create(self, validated_data):
        user = self.context['request'].user
        category = validated_data.pop('category')
        post = Post.objects.create(category=category, **validated_data)
        return post


class PostUpdateSerializer(serializers.ModelSerializer):
    """

    Serializer for updating a post.

    Fields:
    - title
    - content
    - category
    - image

    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']


class PostStatusChangeSerializer(serializers.ModelSerializer):
    """

    Serializer for changing the status of a post (published/hidden).

    Fields:
    - status

    """
    class Meta:
        model = Post
        fields = ['status']


class PostLikeSerializer(serializers.Serializer):
    """

    Serializer for liking/unliking a post.

    Fields:
    - liked
    - likes_count

    """
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()


class CommentCreateSerializer(serializers.ModelSerializer):
    """

    Serializer for creating a new comment.

    Fields:
    - id
    - author
    - content
    - date

    """
    id = serializers.IntegerField(source='pk', read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'date']


class PostSearchSerializer(serializers.ModelSerializer):
    """

    Serializer for searching posts.

    Fields:
    - All fields of Post model

    """
    class Meta:
        model = Post
        fields = '__all__'


class PostCategorySerializer(serializers.ModelSerializer):
    """

    Serializer for representing posts by category.

    Fields:
    - All fields of Post model

    """
    class Meta:
        model = Post
        fields = '__all__'
