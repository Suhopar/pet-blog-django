from django.db import models
from django.conf import settings


# Create your models here.
class Category(models.Model):
    """

    Model representing categories for posts.

    Fields:
        title (CharField)

    """

    title = models.CharField(
        verbose_name='title',
        max_length=255,
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    """

    Model representing a post.

    Fields:
        title (CharField)
        content (CharField)
        category (ForeignKey)
        image (ImageField)
        date (DateField)
        author (ForeignKey)
        likes (ManyToManyField)
        status (CharField) (published or hidden)

    """
    title = models.CharField(
        verbose_name='title',
        max_length=255
    )
    content = models.CharField(
        verbose_name='content',
        max_length=2048
    )
    category = models.ForeignKey(
        Category,
        verbose_name='category',
        on_delete=models.CASCADE,
        null=True
    )

    image = models.ImageField(
        upload_to='post_images/',
        null=True,
        blank=True
    )

    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_like')

    STATUS_CHOICES = [
        ('published', 'Published'),
        ('hidden', 'Hidden'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()



class Comment(models.Model):
    """

    Model representing comments on posts.

    Fields:
        post (ForeignKey)
        author (ForeignKey)
        content (TextField)
        date (DateTimeField)
        likes (ManyToManyField)
        status (CharField) (published or hidden)

    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField(
        verbose_name='content',
        max_length=120
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_like')

    STATUS_CHOICES = [
        ('published', 'Published'),
        ('hidden', 'Hidden'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def number_of_likes(self):
        return self.likes.count()