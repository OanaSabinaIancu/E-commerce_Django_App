# Generated by Django 3.2.6 on 2022-06-15 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0051_remove_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewproduct',
            name='published',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]