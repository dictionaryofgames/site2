from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        return '/static/images/placeholder.png'


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id}'

    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'