from .models import Category


def category_list(request):
    return {
        "category_urls": [
            {"title": category.title, "id": category.id}
            for category in Category.objects.all()
        ]
    }