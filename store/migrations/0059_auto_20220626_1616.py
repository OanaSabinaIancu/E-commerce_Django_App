# Generated by Django 3.2.6 on 2022-06-26 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0058_alter_reviewproduct_reviewprod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='password2',
        ),
    ]
