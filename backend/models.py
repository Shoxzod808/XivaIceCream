from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=50)
    expiration_date = models.DateField()
    manufacture_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.flavor})"

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} items"

class Order(models.Model):
    date_ordered = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='new')  # Example statuses: new, processing, completed
    delivery_date = models.DateField()

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"

class User(models.Model):
    username = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=100)
    role = models.CharField(max_length=50)  # Example roles: admin, warehouse_worker

    def __str__(self):
        return self.username
