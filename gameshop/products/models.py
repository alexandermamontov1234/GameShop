import decimal
import uuid
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse
from profiles.models import Profile
from django.db.models import Avg
from django.template.defaultfilters import slugify


def get_random_code():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code


class Product(models.Model):
    title = models.CharField(max_length=150, blank=True, verbose_name='Название товара')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, verbose_name='Цена товара')
    image = models.ImageField(default='products/defaultgame.png', upload_to='products', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')
    discount = models.FloatField(blank=True, default=0)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    favorite = models.ManyToManyField(Profile, blank=True, related_name='favorites')
    shopping_cart = models.ManyToManyField(Profile, blank=True, related_name='shopping_cart')

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('products', kwargs={'product_slug': self.slug})

    @property
    def get_final_price(self):
        return self.price / 100 * (100 - decimal.Decimal(self.discount))

    def get_rating(self):
        return list(self.review_set.all().aggregate(Avg('rate')).values())[0]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], verbose_name='Рейтинг')
    body = models.TextField(max_length=1500, verbose_name='Отзыв')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True, db_index=True, verbose_name='URL')
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
