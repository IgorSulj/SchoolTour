from django.contrib import admin
from .models import Category, Departure, Tour, TourDay, Date

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['__str__', 'is_top_category', 'is_active']
    list_editable = ['is_top_category', 'is_active']


@admin.register(Departure)
class DepartureAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TourDayInline(admin.StackedInline):
    model = TourDay


class DateInline(admin.TabularInline):
    model = Date


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'departure', 'is_top_tour', 'is_active']
    list_editable = ['is_top_tour', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourDayInline, DateInline]


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    pass
