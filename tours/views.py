from django.core.paginator import Paginator
from django.views.generic import ListView
from django.shortcuts import render

from .models import Category, Date, Tour
from .functions import sort_dates

# Create your views here.
        


def category_view(request, slug=None):
    page = request.GET.get("page", 1)
    categories = Category.objects.filter(is_active=True)
    tours = Tour.objects.filter(is_active=True) if slug is None else Tour.objects.filter(category__slug=slug, category__is_active=True, is_active=True)
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


class TourDestinationView(ListView):
    model = Tour
    page_kwarg = 'page'
    paginate_by = 9
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = context['page_obj']
        context['categories'] = Category.objects.filter(destination__slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return super().get_queryset().filter(category__destination__slug=self.kwargs['slug']).order_by('pk')
