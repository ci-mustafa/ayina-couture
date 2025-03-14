# Generated by Django 5.1.4 on 2025-01-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_available_sizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green'), ('yellow', 'Yellow'), ('black', 'Black'), ('white', 'White'), ('pink', 'Pink'), ('purple', 'Purple'), ('orange', 'Orange'), ('brown', 'Brown'), ('gray', 'Gray'), ('beige', 'Beige'), ('navy', 'Navy'), ('teal', 'Teal'), ('violet', 'Violet')], default=None, max_length=10, null=True),
        ),
    ]
