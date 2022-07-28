from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Category, Tour

# Create your views here.

def category_view(request, slug=None):
    page = request.GET.get("page", 1)
    categories = Category.objects.all()
    tours = Tour.objects.all() if slug is None else Tour.objects.filter(category__slug=slug)
    paginator = Paginator(tours, 9)
    page = paginator.get_page(page)
    context = {'categories': categories, 'paginator': paginator, 'page': page, 'slug': slug}
    return render(request, 'category.html', context)
