# Generated by Django 5.1.4 on 2025-01-16 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickcheckout', '0003_order_original_cart_order_stripe_pid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='original_cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='stripe_pid',
        ),
    ]
