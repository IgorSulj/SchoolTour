from django.urls import path
from django.views.generic import DetailView
from .models import Tour
from .views import category_view

app_name = 'tours'

urlpatterns = [
    path('', category_view, name='main_page'),
    path('categories/<slug:slug>/', category_view, name='category'),
    path('tours/<slug:slug>', DetailView.as_view(model=Tour, template_name='tour.html'), name='tour'),
]