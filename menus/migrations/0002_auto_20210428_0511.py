# Generated by Django 3.0.8 on 2021-04-28 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
