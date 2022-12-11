from django.db.models import F, Value, SlugField
from django.db.models.functions import ConcatPair
from .models import Tour, Category

def hot_links(_):
    top_tour_links = Tour.objects.filter(is_top_tour=True) \
        .annotate(link=ConcatPair(Value('/tours/'), F('slug'), output_field=SlugField())) \
        .values_list('name', 'link', named=True)
    top_category_links = Category.objects.filter(is_top_category=True) \
        .annotate(link=ConcatPair(Value('/categories/'), F('slug'), output_field=SlugField())) \
        .values_list('name', 'link', named=True)
    hot_links = top_tour_links.union(top_category_links)
    return {'hot_links': hot_links}