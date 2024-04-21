from django.db import models
from django.utils import timezone
class Product(models.Model):
    photo = models.ImageField(
        upload_to='media/', 
        null=True, 
        blank=True, 
        default='media/default.jpg',
        verbose_name='rasm'
    )

    name = models.CharField(max_length=255, verbose_name='nomi')
    price = models.IntegerField(verbose_name='narxi')
    count = models.IntegerField(verbose_name='qoldiq')
    
    class Meta:
        verbose_name = 'maxsulot'
        verbose_name_plural = 'maxsulotlar'

    def __str__(self):
        return f"{self.name} ({self.flavor})"

class InventoryProduct(models.Model):
    product = models.ForeignKey('Product', related_name='Product', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='soni')
    inventory = models.ForeignKey('Inventory', related_name='Inventory', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'kirim(maxssulot)'
        verbose_name_plural = 'kirim(maxssulot)'

    def __str__(self):
        return f"{self.product}"

class Inventory(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'kirim'
        verbose_name_plural = 'kirim'

    def __str__(self):
        return f"{self.created_date}"

class Driver(models.Model):
    name = models.CharField(max_length=255, verbose_name='FIO')
    phone = models.CharField(max_length=255, verbose_name='Telefon')
    auto = models.CharField(max_length=255, verbose_name='Avtomobil')

    class Meta:
        verbose_name = 'xaydovchi'
        verbose_name_plural = 'xaydovchilar'

class OrderProduct(models.Model):
    product = models.ForeignKey('Product', related_name='ProductFromOrder', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='soni')
    order = models.ForeignKey('Order', related_name='Order', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'chiqim(maxssulot)'
        verbose_name_plural = 'chiqim(maxssulot)'

    def __str__(self):
        return f"{self.product}"

class Order(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey('Driver', related_name='Driver', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0, verbose_name='Summa')
    STATUS_CHOICES = (
        ('Jarayonda', 'Jarayonda'),
        ('Yakunlandi', 'Yakunlandi'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Jarayonda'
    )

    class Meta:
        verbose_name = 'chiqim'
        verbose_name_plural = 'chiqim'

    def __str__(self):
        return f"{self.created_date}"   

class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    role = models.CharField(max_length=50)  # Example roles: admin, warehouse_worker

    def __str__(self):
        return self.username
