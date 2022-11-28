from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Category, Date, Tour
from .functions import sort_dates

# Create your views here.
        


def category_view(request, slug=None):
    page = request.GET.get("page", 1)
    categories = Category.objects.filter(is_active=True)
    tours = Tour.objects.filter(is_active=True) if slug is None else Tour.objects.filter(category__slug=slug, categories__is_active=True, is_active=True)
    tours = tours.order_by('pk')
    paginator = Paginator(tours, 9)
    page = paginator.get_page(page)
    context = {'categories': categories, 'paginator': paginator, 'page': page, 'slug': slug}
    return render(request, 'category.html', context)


def calendar_view(request):
    dates_list = Date.objects.filter(tour__is_active=True).select_related('tour')
    months = sort_dates(dates_list)
    context = {'months': months}
    return render(request, 'calendar.html', context)

