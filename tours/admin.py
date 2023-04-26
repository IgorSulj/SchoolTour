from django.contrib import admin
from django.core.exceptions import ValidationError
from .functions import count
from .models import TourDestination, Category, Departure, Tour, TourDay, Date

# Register your models here.


@admin.register(TourDestination)
class TourDestinationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['__str__', 'is_main']
    list_editable = ['is_main']

    def get_changelist_formset(self, request, **kwargs):
        FormSet = super().get_changelist_formset(request, **kwargs)

        class TourDestinationFormSet(FormSet):
            def clean(self):
                super().clean()
                main_count = count(dest for dest in self.cleaned_data if dest['is_main'])
                if main_count > 1:
                    raise ValidationError('Главный тур уникален.')
        
        return TourDestinationFormSet
 

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
    actions = ['fill_tours_without_destination']

    @admin.action(description='Выставить все из выделенных туров с незаполнеными полями страны как туры по Беларуси')
    def fill_tours_without_destination(self, request, queryset):
        main_destination = TourDestination.objects.get(is_main=True)
        queryset.filter(destination=None).update(destination=main_destination)


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    pass
