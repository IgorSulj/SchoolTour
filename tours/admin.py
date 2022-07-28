from pyexpat import model
from django.contrib import admin
from .models import Category, Tour, TourDay, Date

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class TourDayInline(admin.StackedInline):
    model = TourDay


class DateInline(admin.TabularInline):
    model = Date


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TourDayInline, DateInline]


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    pass
