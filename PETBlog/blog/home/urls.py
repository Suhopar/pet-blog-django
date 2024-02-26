from django.urls import path, include
from .views import (
    Index,
    PostDetailView,
    PostCreateView,
    RemovePostView,
    PostUpdateView,
    PostStatusChangeView,
    SearchView,
    CategoryView,
    PostLikeView,
    TopTenView,
    CommentCreateView,
    RemoveCommentView,
    CommentLikeView,
    AboutView
)
"""


- index

<int:pk>/
- Page of publication.

post_create/
- Page to create a publication.

remove_post/<pk>/
- To remove a publication.

post/<int:pk>/edit/
- Page to edit the publication.

post/<int:pk>/change_status/
- To change the status of a publication (published/hidden).

like/<int:pk>/
- To like the publication.

post/<int:pk>/comment/
- For commenting on a publication.

comment/<int:pk>/remove/
- To remove a comment.

search/
- A page with a list of the result of the publication search.

category/<pk>/
- A page with a list of all publications with a specific category.

about/
- A page with information about the project.

"""
urlpatterns = [
    path('', Index.as_view(), name='index'),

    path('<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post_create/', PostCreateView.as_view(), name='post-create'),
    path('remove_post/<pk>/', RemovePostView.as_view(), name='remove-post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),

    path('post/<int:pk>/change_status/', PostStatusChangeView.as_view(), name='post-change-status'),
    path('like/<int:pk>/', PostLikeView.as_view(), name='post-like'),


    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add-comment'),
    path('comment/<int:pk>/remove/', RemoveCommentView.as_view(), name='remove-comment'),
    path('like_comment/<int:pk>/', CommentLikeView.as_view(), name='like-comment'),

    path('top_ten/', TopTenView.as_view(), name='top-ten'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<pk>/', CategoryView.as_view(), name='category'),

    path('about/', AboutView.as_view(), name='about'),
]
