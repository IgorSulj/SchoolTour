import datetime
from time import strftime
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)
    is_top_category = models.BooleanField(verbose_name='Отображать в меню?', db_index=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tour(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tours', verbose_name='Категория')
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)
    image = models.ImageField(upload_to='tours/titles/%Y/%m/%d', verbose_name='Титульное фото', blank=True, null=True)
    subname = models.CharField(max_length=150, verbose_name='Подзаголовок')
    price = models.CharField(max_length=50, verbose_name='Цена')
    price_includes = models.TextField(verbose_name='В стоимость входит')
    addons = models.TextField(verbose_name='Дополнительно оплачивается')
    is_top_tour = models.BooleanField(verbose_name='Отображать в меню?', db_index=True, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'


class TourDay(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='days', verbose_name='Тур')
    day_number = models.IntegerField(verbose_name='Номер дня')
    description = models.TextField(verbose_name='Описание')
    img1 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 1', blank=True, null=True)
    img2 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 2', blank=True, null=True)
    img3 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 3', blank=True, null=True)
    img4 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 4', blank=True, null=True)

    def all_images(self):
        return filter(None, (self.img1, self.img2, self.img3, self.img4))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tour', 'day_number'], name='unique day per tour')
        ]
        ordering = ['day_number']
        verbose_name = 'День тура'
        verbose_name_plural = 'Дни тура'


class Date(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, verbose_name='Тур', related_name='dates')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата конца')
    date_price = models.CharField(max_length=50, null=True, blank=True, verbose_name='Цена')
    places = models.IntegerField(verbose_name='Места')

    @property
    def price(self):
        return self.date_price or self.tour.price

    def __str__(self) -> str:
        result = self.start_date.strftime('%d.%m.%Y')
        if self.end_date:
            result = result + '-' + self.end_date.strftime('%d.%m.%Y')
        return f'{self.tour} ({result})'

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'
        ordering = ['start_date', 'end_date']

