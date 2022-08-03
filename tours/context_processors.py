from .models import Tour

def top_tours(request):
    return {'top_tours': Tour.objects.filter(is_top_tour=True)}