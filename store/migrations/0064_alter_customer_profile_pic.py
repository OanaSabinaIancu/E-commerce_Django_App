# Generated by Django 3.2.6 on 2022-06-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0063_alter_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/profil3.jpg', upload_to=''),
        ),
    ]
