# Generated by Django 5.0.3 on 2024-04-27 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='price',
            field=models.IntegerField(default=1, verbose_name='Narxi'),
            preserve_default=False,
        ),
    ]