from typing import Any, Optional
from django.core.paginator import Paginator
from django.db import models
from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Category, Date, Tour, TourDestination
from .functions import sort_dates

# Create your views here.
        


def category_view(request, slug=None):
    page = request.GET.get("page", 1)
    categories = Category.objects.filter(is_active=True)
    tours = Tour.active.all() if slug is None else Tour.active.filter(category__slug=slug)
    tours = tours.order_by('pk')
    paginator = Paginator(tours, 9)
    page = paginator.get_page(page)
    context = {'categories': categories, 'paginator': paginator, 'page': page, 'slug': slug}
    return render(request, 'category.html', context)


def calendar_view(request):
    dates_list = Date.objects.filter(tour__is_active=True, tour__category__is_active=True).select_related('tour')
    months = sort_dates(dates_list)
    context = {'months': months}
    return render(request, 'calendar.html', context)


class TourDestinationView(DetailView):
    model = TourDestination
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    context_object_name = 'destination'
    template_name = 'category.html'

    def get_tours_paginator(self):
        page = int(self.request.GET.get('page', 1))
        tours = Tour.active.filter(category__destination__slug=self.kwargs['slug']).order_by('pk')
        paginator = Paginator(tours, 9)
        page = paginator.get_page(page)
        return {'paginator': paginator, 'page': page}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.object.categories.all()
        context.update(self.get_tours_paginator())
        return context
