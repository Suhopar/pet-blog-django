from rest_framework import serializers
from accounts.models import CustomUser
from api.home.serializers import PostListSerializer, CommentSerializer
from home.models import Category, Post, Comment


class UserRegisterSerializer(serializers.Serializer):
    """

    Serializer for registering a user.

    Fields:
    - username
    - email
    - password1
    - password2
    - first_name
    - last_name

    Methods:
    - validate
    - create

    JSON:
    {
    "username": "tst",
    "email": "tst@example.com",
    "password1": "Password123*",
    "password2": "Password123*",
    "first_name": "Tst",
    "last_name": "Tstonsky"
    }

    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """

    Serializer for user login.

    Fields:
    - username
    - password

    JSON:
    {
    "username": "tst",
    "password": "Password123*"
    }

    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})


class ProfileSerializer(serializers.ModelSerializer):
    """

    Serializer for user profile.

    Fields:
    - id
    - username
    - first_name
    - last_name
    - email
    - role
    - posts

    Methods:
    - get_posts

    JSON:
    {
        "id": 1,
        "username": "usertst",
        "first_name": "Tstian",
        "last_name": "Tstovsky",
        "email": "usertst@gmail.com",
        "role": "admin",
        "posts": [
            {
                "id": 33,
                "title": "la la la upd",
                "content": "bla vla ",
                "image": "/media/post_images/regular-magic-ox4RB.jpg",
                "date": "2023-09-18",
                "status": "published",
                "category": 3,
                "author": 1,
                "likes": [
                    1,
                    5
                ]
            },
            {
                "id": 43,
                "title": "api tst with img",
                "content": "lol lol lol lol lolo",
                "image": "/media/post_images/yami-yami-15_6zekn6r.jpg",
                "date": "2023-09-26",
                "status": "published",
                "category": 1,
                "author": 1,
                "likes": []
            }
        ]
    }

    """
    posts = serializers.SerializerMethodField()


    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'posts']


    def get_posts(self, obj):
        posts = obj.post_set.all()
        return PostListSerializer(posts, many=True).data


class UserListSerializer(serializers.ModelSerializer):
    """

    Serializer for listing users.

    Fields:
    - id
    - username
    - num_posts
    - date_joined
    - role
    - is_staff

    Methods:
    - get_num_posts

    JSON:
    [
    {
        "id": 4,
        "username": "test1",
        "num_posts": 1,
        "date_joined": "2023-09-08T15:19:02.736214Z",
        "role": "user",
        "is_staff": false
    },
    {
        "id": 5,
        "username": "test2",
        "num_posts": 1,
        "date_joined": "2023-09-18T14:13:39.191197Z",
        "role": "admin",
        "is_staff": false
    },
    {
        "id": 1,
        "username": "usertst",
        "num_posts": 9,
        "date_joined": "2023-09-08T14:42:03Z",
        "role": "admin",
        "is_staff": true
    },
    {
        "id": 6,
        "username": "test3",
        "num_posts": 0,
        "date_joined": "2023-09-21T15:31:55.184647Z",
        "role": "user",
        "is_staff": false
    }
    ]
    """
    num_posts = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'num_posts', 'date_joined', 'role', 'is_staff']

    def get_num_posts(self, obj):
        return obj.post_set.count()


class AdminPostListSerializer(serializers.ModelSerializer):
    """

    Serializer for listing posts in the admin panel.

    Fields:
    - id
    - title
    - author
    - category
    - date
    - status
    - likes
    - comments_count

    Methods:
    - get_comments_count

    JSON:
    [
    {
        "id": 33,
        "title": "la la la upd",
        "author": 1,
        "category": 3,
        "date": "2023-09-18",
        "status": "published",
        "likes": [
            1,
            5
        ],
        "comments_count": 5
    },
    {
        "id": 43,
        "title": "api tst with img",
        "author": 1,
        "category": 1,
        "date": "2023-09-26",
        "status": "published",
        "likes": [],
        "comments_count": 0
    },
    {
        "id": 31,
        "title": "img",
        "author": 1,
        "category": 1,
        "date": "2023-09-17",
        "status": "published",
        "likes": [
            1,
            4,
            6
        ],
        "comments_count": 3
    }
    ]

    """
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'category', 'date', 'status', 'likes', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comment_set.count()