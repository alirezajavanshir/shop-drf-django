# Generated by Django 5.1.1 on 2024-10-15 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_created_at'),
        ('shop', '0002_discountcode_cart_product_cartitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='shop.product'),
        ),
    ]
