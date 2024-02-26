from django.contrib import admin
from .models import Post, Category, Comment


# Register your models here.
def publish_posts(modeladmin, request, queryset):
    queryset.update(status='published')


publish_posts.short_description = "Publish selected posts"


def hide_posts(modeladmin, request, queryset):
    queryset.update(status='hidden')


hide_posts.short_description = "Hide selected posts"


# admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """

    Admin interface for managing posts.

    """
    list_display = ('id', 'title', 'author', 'date', 'status')
    search_fields = ('author__username', 'title')
    list_filter = ('date', 'category', 'author')
    readonly_fields = ('id', 'date')
    actions = (publish_posts, hide_posts)
    fieldsets = [
        (None, {'fields': ['title', 'content', 'category']}),
        ('Advanced options', {'fields': ['status', 'image'], 'classes': ['collapse']}),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """

    Admin interface for managing categories.

    """
    list_display = ('id', 'title')
    readonly_fields = ('id',)


def publish_comments(modeladmin, request, queryset):
    queryset.update(status='published')


publish_comments.short_description = "Publish selected comments"


def hide_comments(modeladmin, request, queryset):
    queryset.update(status='hidden')


hide_comments.short_description = "Hide selected comments"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """

    Admin interface for managing comments.

    """
    list_display = ('id', 'author', 'post', 'date', 'status')
    search_fields = ('author__username', 'post__title')
    list_filter = ('date', 'post__title', 'author')
    readonly_fields = ('id', 'date')
    actions = (publish_comments, hide_comments)
