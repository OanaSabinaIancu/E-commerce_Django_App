# Generated by Django 3.2.6 on 2022-06-23 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0053_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecoverEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]