from .models import Category


# this is a context processor that category shows throughout the app
def categories(request):
    categories = Category.objects.all()
    return {"categories": categories}
