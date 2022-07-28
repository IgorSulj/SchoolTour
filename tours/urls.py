from django.urls import path
from .views import category_view

app_name = 'tours'

urlpatterns = [
    path('', category_view, name='main_page'),
    path('categories/<slug:slug>/', category_view, name='category')
]