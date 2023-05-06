from django.db import models
from django.db.transaction import atomic
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create your models here.

class TourDestination(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)
    full_name = models.CharField(max_length=150, verbose_name='Полное название', blank=True, null=True)
    is_main = models.BooleanField(default=False, verbose_name='Главная страна?')
    description = models.TextField(verbose_name='Описание', default='')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def page_header(self):
        return self.full_name or self.name
    
    def get_absolute_url(self):
        return reverse("tours:destination", kwargs={"slug": self.slug})
    

class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(models.Model):
    destination = models.ForeignKey(TourDestination, on_delete=models.PROTECT, verbose_name='Страна', related_name='categories',
                                    db_index=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)
    is_top_category = models.BooleanField(verbose_name='Отображать в меню?', db_index=True, default=False)
    is_active = models.BooleanField(verbose_name='Активная категория?', db_index=True, default=True)

    objects = models.Manager()
    active = ActiveCategoryManager()

    def get_absolute_url(self):
        return reverse("tours:category", kwargs={'slug': self.slug})
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Departure(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Выезд'
        verbose_name_plural = 'Выезды'


class ActiveTourManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, category__is_active=True)


class Tour(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tours', verbose_name='Категория')
    departure = models.ForeignKey(Departure, on_delete=models.PROTECT, related_name='tours', verbose_name='Выезд', null=True)
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='URI', db_index=True)
    image = models.ImageField(upload_to='tours/titles/%Y/%m/%d', verbose_name='Титульное фото', blank=True, null=True)
    image_alt = models.CharField(max_length=75, verbose_name='Alt-тег титульного фото', blank=True, null=True)
    subname = models.CharField(max_length=150, verbose_name='Подзаголовок')
    price = models.CharField(max_length=50, verbose_name='Цена')
    price_includes = models.TextField(verbose_name='В стоимость входит')
    addons = models.TextField(verbose_name='Дополнительно оплачивается')
    is_top_tour = models.BooleanField(verbose_name='Отображать в меню?', db_index=True, default=False)
    is_active = models.BooleanField(verbose_name='Активный тур?', db_index=True, default=True)

    objects = models.Manager()
    active = ActiveTourManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'

    def get_absolute_url(self):
        return reverse('tours:tour', kwargs={'slug': self.slug})
    


class TourDay(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='days', verbose_name='Тур')
    day_number = models.IntegerField(verbose_name='Номер дня')
    description = models.TextField(verbose_name='Описание')
    img1 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 1', blank=True, null=True)
    img1_alt = models.CharField(max_length=75, verbose_name='Alt-тег фото 1', blank=True, null=True)
    img2 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 2', blank=True, null=True)
    img2_alt = models.CharField(max_length=75, verbose_name='Alt-тег фото 2', blank=True, null=True)
    img3 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 3', blank=True, null=True)
    img3_alt = models.CharField(max_length=75, verbose_name='Alt-тег фото 3', blank=True, null=True)
    img4 = models.ImageField(upload_to='tours/days/%Y/%m/%d', verbose_name='Фото 4', blank=True, null=True)
    img4_alt = models.CharField(max_length=75, verbose_name='Alt-тег фото 4', blank=True, null=True)

    def all_images(self):
        print(self.img2)
        if self.img1:
            yield (self.img1, self.img1_alt)
        if self.img2:
            yield (self.img2, self.img2_alt)
        if self.img3:
            yield (self.img3, self.img3_alt)
        if self.img4:
            yield (self.img4, self.img4_alt)

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

