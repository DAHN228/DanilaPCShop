from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Type'
        verbose_name_plural = 'Types'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_type',
                       args=[self.slug])


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_brand',
                       args=[self.slug])


class Backlight(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Backlight'
        verbose_name_plural = 'Backlights'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_backlight',
                       args=[self.slug])


class Product(models.Model):
    type = models.ForeignKey(Type, related_name='products', default='0000000',
                             on_delete=models.CASCADE, )
    brand = models.ForeignKey(Brand, related_name='brands', default='0000000',
                              on_delete=models.CASCADE, )
    backlight = models.ForeignKey(Backlight, related_name='lights', default='0000000',
                                 on_delete=models.CASCADE, )
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id, self.slug])


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Review for {self.product} by {self.user}"
    def get_review_author(self):
        return self.user