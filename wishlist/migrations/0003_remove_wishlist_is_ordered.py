# Generated by Django 5.1.4 on 2025-01-22 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_wishlist_is_ordered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='is_ordered',
        ),
    ]
