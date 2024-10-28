# Generated by Django 5.1.2 on 2024-10-28 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_product_order_orderitem_order_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approve', 'Approved')], default='Pending', max_length=10),
        ),
    ]
