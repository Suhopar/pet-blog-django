from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, TemplateView, FormView, UpdateView
from .models import Post, Category, Comment
from .forms import PostForm, SearchForm, CommentForm
from django.core.paginator import Paginator


def paginate_queryset(request, queryset, per_page=10):
    """

    Function for paginating a queryset.

    request - The current HTTP request.
    queryset - The queryset to be paginated.
    per_page - Number of items per page (default is 10).

    return - Paginated queryset.

    """
    page_number = request.GET.get('page')
    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)
    return page_obj


# Create your views here.
class Index(TemplateView):
    """

    View for rendering the index page.
    Sends a list of all publications to the index page.

    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.filter(status='published').order_by('-date')
        context['post_list'] = paginate_queryset(self.request, post_list, per_page=10)

        return context


class PostDetailView(DetailView):
    """

    View for displaying a detailed view of a post.
    This view displays the publication and its associated comments, as well as the number of likes.

    """
    template_name = 'post_page.html'
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        post = Post.objects.get(id=self.kwargs.get('pk'))
        context['post'] = post

        context['comments'] = Comment.objects.filter(post=post)
        context['comment_form'] = CommentForm()

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        for comment in context['comments']:
            comment.liked = comment.likes.filter(id=self.request.user.id).exists()

        context['number_of_likes'] = post.number_of_likes()
        context['post_is_liked'] = liked

        return context

    def dispatch(self, *args, **kwargs):
        post = self.get_object()
        if post.status == 'hidden' and not (self.request.user.is_authenticated and (
                self.request.user == post.author or self.request.user.role == 'admin')):
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class PostCreateView(FormView):
    """

    The view for creating a new publication.
    This view displays the form for creating a new publication and handles the submission of the form.

    """
    template_name = 'post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context

    def form_valid(self, form):
        user = self.request.user
        category_id = self.request.POST.get('category')
        category = Category.objects.filter(pk=category_id).first()

        if not category:
            form.add_error('category', 'Invalid category selected.')
            return self.form_invalid(form)

        post = form.save(commit=False)
        post.author = user
        post.category = category
        if 'image' in self.request.FILES:
            post.image = self.request.FILES['image']
        post.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class RemovePostView(View):
    """

    View for removing a post.
    This view handles the removal of a post, either by the author or an admin.

    """

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.filter(pk=pk).first()
        user = self.request.user
        referer = request.META.get('HTTP_REFERER')
        if post.author == user or user.role == 'admin':
            post.delete()

        if not referer.endswith('/account/admin-post-list/') and not '/account/profile/' in referer and not '/account/admin-post-list/?page=' in referer:
            return redirect('index')
        else:
            return redirect(referer)

    def dispatch(self, *args, **kwargs):
        post = Post.objects.filter(id=self.kwargs.get('pk')).first()
        if not self.request.user.is_authenticated or (
                post.author.id != self.request.user.id and self.request.user.role != 'admin'):
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class PostUpdateView(UpdateView):
    """

    View for updating a post.
    This view displays the form for updating a post and handles the submission of the form.
    Only author or admin.

    """
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'content', 'category', 'image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = Post.objects.filter(id=self.kwargs.get('pk')).first().author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.object.pk})

    def dispatch(self, *args, **kwargs):
        post = Post.objects.filter(id=self.kwargs.get('pk')).first()
        if not self.request.user.is_authenticated or (
                post.author.id != self.request.user.id and self.request.user.role != 'admin'):
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class PostStatusChangeView(View):
    """

    View for changing the status of a post.
    This view handles changing the status of a post (published or hidden).
    Only author or admin.

    """
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        status = self.request.GET.get('status')
        referer = request.META.get('HTTP_REFERER')

        post = Post.objects.filter(pk=pk).first()
        user = self.request.user

        if post and (post.author == user or user.role == 'admin'):
            post.status = status
            post.save()

        return redirect(referer)

    def dispatch(self, *args, **kwargs):
        post = Post.objects.filter(id=self.kwargs.get('pk')).first()
        if not self.request.user.is_authenticated or (
                post.author.id != self.request.user.id and self.request.user.role != 'admin'):
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class PostLikeView(View):
    """

    View for handling post likes.
    This view handles both liking and unliking a post.

    """
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        # ajax
        likes_count = post.likes.count()
        return JsonResponse({'liked': liked, 'likes_count': likes_count})
        # default
        # return HttpResponseRedirect(reverse('post', args=[str(pk)]))

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class CommentCreateView(View):
    """

    View for creating a new comment.
    This view handles both creating and rendering comments.

    """
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.content = request.POST.get('comment_content')
            comment.save()

            # ajax
            return JsonResponse({
                'comment_id': comment.id,
                'author_username': comment.author.username,
                'content': comment.content,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                'remove_comment_url': reverse('remove-comment', kwargs={'pk': comment.pk}),

            })
        else:
            return JsonResponse({'error': 'Invalid form data'}, status=400)
        # default
        # return redirect('post', pk=pk)

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class RemoveCommentView(View):
    """

    View for removing a comment.
    Only author or admin.

    """
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()

        # ajax
        return JsonResponse({'success': True})
        # default
        # return redirect('post', pk=comment.post.pk)

    def dispatch(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get('pk'))
        if not self.request.user.is_authenticated or (
                comment.author.id != self.request.user.id and self.request.user.role != 'admin'):
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class CommentLikeView(View):

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True

        likes_count = comment.likes.count()
        print(comment, "id - ", comment.id, "liked - ", liked, "comment_likes_count - ", likes_count)

        return JsonResponse({'comment_liked': liked, 'comment_likes_count': likes_count})

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)


class SearchView(View):
    """

    View for handling search queries.
    This view renders the search results page.

    """
    template_name = 'search_results.html'

    def get(self, request):
        form = SearchForm(request.GET)
        post_list = None

        if form.is_valid():
            query = form.cleaned_data['query']
            post_list = Post.objects.filter(status='published', title__contains=query)
        # paginated_post_list = paginate_queryset(request, post_list, per_page=10)
        # print('-----------------', paginated_post_list, '=============', post_list)
        return render(request, self.template_name, {'form': form, 'post_list': post_list})


class CategoryView(View):
    """

    View for displaying posts within a specific category.
    This view renders the category page with a list of posts belonging to that category.

    """

    template_name = 'category.html'

    def get(self, request, *args, **kwargs):
        category = Category.objects.filter(id=self.kwargs.get('pk')).first()
        post_list = Post.objects.filter(status='published', category=category)
        paginated_post_list = paginate_queryset(request, post_list, per_page=9)

        return render(request, self.template_name, {'category': category, 'post_list': paginated_post_list})


class TopTenView(View):
    """

    View for displaying the TOP 10 page.

    """
    template_name = 'post_top_ten.html'

    def get(self, request):
        post_list = Post.objects.filter(status='published').annotate(num_likes=Count('likes')).order_by('-num_likes')[:10]
        return render(request, self.template_name, {'post_list': post_list})



class AboutView(View):
    """

    View for displaying the About page.

    """
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)
