# Generated by Django 4.2.5 on 2024-04-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='case',
            field=models.IntegerField(default=1, verbose_name='yashikdagi soni'),
        ),
    ]