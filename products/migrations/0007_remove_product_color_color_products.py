# Generated by Django 5.1.4 on 2025-01-20 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_color_remove_product_color_product_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.AddField(
            model_name='color',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='colors', to='products.product'),
        ),
    ]
