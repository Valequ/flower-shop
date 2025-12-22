from django.db import models
from django.core.validators import MinValueValidator
import os
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-адрес')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Product(models.Model):    
    name = models.CharField(max_length=200, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-адрес')
    description = models.TextField(verbose_name='Описание', blank=True)
    show_on_main = models.BooleanField(
        default=False, 
        verbose_name='Показывать на главной'
    )
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Категория'
    )
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    old_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Старая цена (для скидки)',
        null=True, 
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    image_filename = models.FilePathField(
        path=os.path.join(settings.BASE_DIR, 'static', 'main', 'img', 'flowers'),
        match='.*\.(jpg|jpeg|png|gif)$', 
        recursive=False,
        max_length=200,
        verbose_name='Имя файла изображения',
        help_text='Выберите файл из static/main/img/flowers'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalog:product_detail', args=[self.slug])
    
    def get_main_image_url(self):
        if self.image_filename:
            filename = os.path.basename(self.image_filename)
            return f'/static/main/img/flowers/{filename}'
        return '/static/main/img/decoration/flower.jpg'
    
    @property
    def has_discount(self):
        return self.old_price is not None and self.old_price > self.price
    
    @property
    def discount_percent(self):
        if self.has_discount:
            return int((1 - self.price / self.old_price) * 100)
        return 0