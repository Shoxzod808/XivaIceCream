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

    name = models.CharField(max_length=255, unique=True, verbose_name='nomi')
    price = models.IntegerField(verbose_name='narxi')
    case = models.IntegerField(default=1, verbose_name='yashikdagi soni')
    count = models.IntegerField(default=0, verbose_name='qoldiq')
    
    class Meta:
        verbose_name = 'maxsulot'
        verbose_name_plural = 'maxsulotlar'

    def total_price(self):
        return self.price * self.count * self.case

    def __str__(self):
        return f"{self.name}"

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
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='FIO')
    phone = models.CharField(max_length=255, verbose_name='Telefon')
    auto = models.CharField(max_length=255, verbose_name='Avtomobil')

    class Meta:
        verbose_name = 'xaydovchi'
        verbose_name_plural = 'xaydovchilar'

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    product = models.ForeignKey('Product', related_name='ProductFromOrder', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Narxi')
    count = models.IntegerField(verbose_name='soni')
    order = models.ForeignKey('Order', related_name='Order', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'chiqim(maxsulot)'
        verbose_name_plural = 'chiqim(maxsulot)'

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
        return f"{self.driver}-{self.created_date}"   

class Payment(models.Model):
    order = models.ForeignKey('Order', related_name='OrderForPayment', on_delete=models.CASCADE)
    cash = models.IntegerField(verbose_name='Summa')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order}'

class Refund(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', related_name='OrderForRefund', on_delete=models.CASCADE)
    cash = models.IntegerField(default=0, verbose_name='Summa')

    class Meta:
        verbose_name = 'Vozvrat'
        verbose_name_plural = 'Vozvratlar'

    def __str__(self):
        return f"{self.created_date}" 

class RefundProduct(models.Model):
    product = models.ForeignKey('Product', related_name='ProductForRefund', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Narxi')
    count = models.IntegerField(verbose_name='soni')
    refund = models.ForeignKey('Refund', related_name='Refund', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Vozvrat(maxsulot)'
        verbose_name_plural = 'Vozvratlar(maxsulot)'

    def __str__(self):
        return f"{self.product}"