# Generated by Django 5.1.2 on 2024-11-02 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='roomimage',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_images', to='hotels.room', verbose_name='Номер'),
        ),
        migrations.AddField(
            model_name='room',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='hotels.roomimage', verbose_name='Фотографии номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='amenities',
            field=models.ManyToManyField(blank=True, related_name='room_types', to='hotels.amenity', verbose_name='Удобства типа номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_types', to='hotels.hotel', verbose_name='Отель'),
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotels.roomtype', verbose_name='Тип номера'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('hotel', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='roomtype',
            unique_together={('hotel', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('room_type', 'number')},
        ),
    ]