# Generated by Django 5.1.2 on 2024-11-06 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_roomtype_max_guests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomtype',
            name='max_guests',
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='occupancy',
            field=models.PositiveIntegerField(default=1, verbose_name='Максимальное количество гостей'),
        ),
    ]
