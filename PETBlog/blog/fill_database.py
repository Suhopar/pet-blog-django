import os
import django
from random import choice, randint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from home.models import Category, Post, Comment
from accounts.models import CustomUser


def populate_db():
    # USERS ------------------------------------- -------------------------------------
    # user list
    users_data = [
        {'username': 'test', 'email': 'test@gmail.com', 'password': 'PassWord1102023*',
         'role': 'user', 'first_name': 'Testovion', 'last_name': 'Testonti'},
    ]

    # create users
    user = CustomUser.objects.create_user(
        username='adminuser',
        password='AdminU0110*',
        role='admin',
        first_name='Admin',
        last_name='Userinsky',
        is_staff=True
    )
    print(f'SuperUser {user.username} created.')

    for i in range(10):  # count - 10
        user = CustomUser.objects.create_user(
            username=f'testuser{i}',
            email=f'autotest{i}@gmail.com',
            password='PassWord1102023*',
            role='user',
            first_name=f'Testovion{i}',
            last_name=f'Testonti{i}',
        )
        print(f'User {user.username} created.')

    # CATEGORY ------------------------------------- -------------------------------------
    # category list (12)
    categories_data = [
        {'title': 'Pets'},
        {'title': 'Politics'},
        {'title': 'Movies'},
        {'title': 'Books'},
        {'title': 'Art'},
        {'title': 'Music'},
        {'title': 'Science'},
        {'title': 'Business'},
        {'title': 'Sports'},
        {'title': 'Health'},
        {'title': 'Food'},
        {'title': 'Travel'},
    ]

    # create category
    for data in categories_data:
        Category.objects.create(title=data['title'])
        print(f'Category {data["title"]} created.')

    # POSTS ------------------------------------- -------------------------------------
    # titles, contents list (4)
    titles = ['Bla bla bla', 'Lo lo lo', 'La la la', 'To to to']
    contents = [
        'Bla, bla, bla! Bla blabl, bla bla, bla blabla bla! Bla blablablabla, bla bla blabl! Bla blablablabla bla blablablabla bla blablablabla bla, blabl? Bla blabla, blablabla! Bla blabl, bla! Bla blablablabla bla blablablabla bla blablablabla bla blabla bla blablablabla bla blablablabla, blablabla bla! Bla blabl, blabla, blabl, bla! Bla blablablabla, bla blablablabla bla blabl! Bla blablablabla bla blabl, blablabla bla blablablabla, blabl! Blabl bla blablablabla bla blablablabla bla blablablabla bla, blabla? Bla blablablabla, bla blablablabla, bla blabl, bla! Bla blablablabla bla blabla bla blablablabla bla blablablabla, blablabla bla! Bla blabl, blabla, blabl, bla! Bla blablabla, bla blablablabla bla blabl! Bla blablablabla bla blabl, blablabla bla blabl! Bla blablablabla bla blabl, bla blabl, blablablabla bla! Bla blablablabla, bla blablablabla, bla blabl, bla! Bla blablablabla bla blabl, blabla bla blablablabla bla blablablabla, blablabla bla! Bla blablablabla bla blabl, blabl, bla! Bla blablablabla bla blabl, bla blabl, blablablabla bla! Bla blablablabla bla blabla bla blablablabla, blabl! Bla blablablabla, bla blablablabla bla blablablabla bla blabla bla blabl, blabl? Bla blablablabla bla blabl, blablabla bla blabl! Bla blablablabla, bla blabl, blablablabla bla! Bla blablablabla, bla blablablabla, bla blabl, bla! Bla blablablabla bla blablablabla bla blablablabla bla blabl bla blablablabla bla blablablabla, blablabla bla! Bla blabl, blabla, blabl, bla! Bla blablablabla bla blabl bla blablablabla, bla! Bla blablablabla bla blabl, bla blabl, blablablabla bla!',
        'Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol! Lo lo lo! Lolo , Loloo, Lol! Lo lo lo, Lolo , Loloo, Lol!',
        'La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal! La la la, Lalaa, Lala , Lalal!',
        'To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot! To to to, Totoo, Toto, Totot!']

    # create posts
    for i in range(50):  # count - 50
        random_number = randint(0, 3)
        category = choice(Category.objects.all())
        author = choice(CustomUser.objects.all())
        title = titles[random_number] + f' {i}'
        content = contents[random_number] + f' {i}'

        post = Post.objects.create(
            title=title,
            content=content,
            category=category,
            author=author,
            image=f'post_images/autoadd_{randint(1, 22)}.jpg'

        )
        print(f'Post {post.title} - {i} created.')

        # add comments to post
        for j in range(5):  # count - 5
            comment = Comment.objects.create(
                post=post,
                author=choice(CustomUser.objects.all()),
                content=f'Lolol {j + 1} bibi {i + 1}'
            )
            print(f'Comment by {comment.author.username} created.')

        # add likes to post
        num_likes = randint(0, 10)
        for k in range(num_likes):
            random_user = choice(CustomUser.objects.all())
            if random_user not in post.likes.all():
                post.likes.add(random_user)
            print(f'Like by {random_user.username} added to post {post.title}.')


if __name__ == '__main__':
    populate_db()
