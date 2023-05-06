from django.urls import path
from django.views.generic import DetailView

from .models import Tour
from .views import main_page, calendar_view, category_view, TourDestinationView

app_name = 'tours'

urlpatterns = [
    path('', main_page, name='main_page'),
    path('categories/<slug:slug>/', category_view, name='category'),
    path('tours/<slug:slug>', DetailView.as_view(model=Tour, template_name='tour.html'), name='tour'),
    path('calendar/', calendar_view, name='calendar'),
    path('<slug:slug>/', TourDestinationView.as_view(), name='destination'),
]
