# Generated by Django 5.1.4 on 2025-01-03 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available_sizes',
        ),
    ]
