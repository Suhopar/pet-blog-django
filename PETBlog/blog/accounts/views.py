from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from django.db.models import Count

from .forms import UserRegisterForm, ProfileEditForm
from .models import CustomUser

from home.models import Post, Comment
from home.views import paginate_queryset


# Create your views here.


class RegisterView(View):
    """

    View for user registration.

    """
    def get(self, request):
        """
        Displays the registration page with an empty form.
        """
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        """
        Handles data from the registration form.
        """
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            role = form.cleaned_data['role']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            usual_ban = form.cleaned_data['usual_ban']
            absolute_ban = form.cleaned_data['absolute_ban']
            user_about = form.cleaned_data['user_about']
            print(form.cleaned_data['profile_image'])
            if 'profile_image' in self.request.FILES:
                profile_image = self.request.FILES['profile_image']
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                    usual_ban=usual_ban,
                    absolute_ban=absolute_ban,
                    profile_image=profile_image,
                    user_about=user_about
                )
            else:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                    usual_ban=usual_ban,
                    absolute_ban=absolute_ban,
                    user_about=user_about
                )

            # user = CustomUser.objects.create_user(
            #     username=username,
            #     email=email,
            #     password=password,
            #     role=role,
            #     first_name=first_name,
            #     last_name=last_name,
            #     usual_ban=usual_ban,
            #     absolute_ban=absolute_ban,
            #     profile_image=profile_image,
            #     user_about=user_about
            # )
            return redirect('index')
        else:
            print(form.errors)


class ProfileEditView(View):
    template_name = 'profile_edit.html'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=self.kwargs.get('pk')).first()
        form = ProfileEditForm(instance=user)
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=self.kwargs.get('pk')).first()
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)
        return render(request, self.template_name, {'form': form, 'user': user})


class ProfileView(View):
    """

    View for displaying a user's profile.

    """
    model = CustomUser
    template_name = 'profile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=self.kwargs.get('pk')).first()
        post_list = Post.objects.filter(author=user).all()
        paginated_post_list = paginate_queryset(request, post_list, per_page=10)
        context = {
            'post_list': paginated_post_list,
            'post_count': (Post.objects.filter(author=user).all()).count(),
            'user_profile': user
        }
        return render(request, self.template_name, context)


class UserListView(ListView):
    """

    View for a page with a list of all users with the ability to sort them into some parameters.

    """
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'user_list'

    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get('sort_by')
        sort_dir = request.GET.get('sort_dir', 'asc')

        if sort_by:
            user_list = self.sort_users(sort_by, sort_dir)
        else:
            user_list = CustomUser.objects.all()

        for user in user_list:
            user.num_posts = user.post_set.count()


        paginated_user_list = paginate_queryset(request, user_list, per_page=10)
        context = {
            'user_list': paginated_user_list,
            'user_count': (CustomUser.objects.all()).count()
        }
        return render(request, self.template_name, context)

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

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')

        if self.request.user.role != 'admin':
            return redirect('index')

        return super().dispatch(*args, **kwargs)


class UserRemoveView(View):
    """

    View to remove a user.

    """
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        referer = request.META.get('HTTP_REFERER')
        user = CustomUser.objects.filter(pk=pk).first()
        current_user = self.request.user

        if current_user.role == 'admin':
            user.delete()

        return redirect(referer)

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')

        if self.request.user.role != 'admin':
            return redirect('index')

        return super().dispatch(*args, **kwargs)


class UserChangeRoleView(View):
    """

    View to change the user role(admin/user).

    """
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        new_role = request.POST.get('new_role')
        referer = request.META.get('HTTP_REFERER')

        user = get_object_or_404(CustomUser, pk=pk)
        current_user = self.request.user

        if current_user.role == 'admin' and new_role in ['admin', 'user']:
            user.role = new_role
            user.save()

        return redirect(referer)

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')

        if self.request.user.role != 'admin':
            return redirect('index')

        return super().dispatch(*args, **kwargs)


class PostListView(ListView):
    """

    View for a page with a list of all publications with the ability to sort by some parameters.

    """
    model = Post
    template_name = 'admin_post_list.html'
    context_object_name = 'admin-post-list'

    def get(self, request, *args, **kwargs):
        sort_by = request.GET.get('sort_by')
        sort_dir = request.GET.get('sort_dir', 'asc')

        if sort_by:
            post_list = self.sort_posts(sort_by, sort_dir)
        else:
            post_list = Post.objects.all()

        paginated_post_list = paginate_queryset(request, post_list, per_page=10)
        context = {
            'post_list': paginated_post_list,
            'post_count': (Post.objects.all()).count()
        }
        return render(request, self.template_name, context)

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
            return Post.objects.annotate(num_likes=Count('likes')).order_by('num_likes' if sort_dir == 'asc' else '-num_likes')
            # return Post.objects.annotate(like_count=Count('likes__id')).order_by(field, 'title').distinct()
        elif sort_by == 'comment':
            return Post.objects.annotate(num_comments=Count('comment')).order_by('num_comments' if sort_dir == 'asc' else '-num_comments')
            # return Post.objects.annotate(comment_count=Count('comment__id')).order_by(field, 'title').distinct()
        elif sort_by == 'hidden':
            return Post.objects.filter(status='hidden')
        elif sort_by == 'published':
            return Post.objects.filter(status='published')
        else:
            return Post.objects.all()

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')

        if self.request.user.role != 'admin':
            return redirect('index')

        return super().dispatch(*args, **kwargs)


class LikedPostsView(View):
    template_name = 'user_like_post_list.html'

    def get(self, request):
        liked_posts = Post.objects.filter(likes=request.user)
        paginated_post_list = paginate_queryset(request, liked_posts, per_page=10)
        context = {
            'post_list': paginated_post_list,
            'post_count': (Post.objects.all()).count()
        }
        return render(request, self.template_name, context)

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(*args, **kwargs)
