from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


def hotel_preview_directory_path(instance, filename):
    return f'hotels/{instance.name}/preview_{filename}'

def hotel_photo_directory_path(instance, filename):
    return f'hotels/{instance.name}/{filename}'

def room_preview_directory_path(instance, filename):
    return f'rooms/{instance.number}/preview_{filename}'

def room_photo_directory_path(instance, filename):
    return f'rooms/{instance.number}/{filename}'


class Hotel(models.Model):
    name = models.CharField(max_length=70, verbose_name='Название отеля')
    address = models.CharField(max_length=80, verbose_name='Адрес отеля')
    city = models.CharField(max_length=70, verbose_name='Город')
    country = models.CharField(max_length=70, verbose_name='Страна')
    description = models.TextField(blank=True, null=True, verbose_name='Описание отеля')
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5.0)], verbose_name='Рейтинг отеля')
    preview = models.ImageField(null=True, blank=True,
                                upload_to=hotel_preview_directory_path,
                                verbose_name='Главное фото отеля')
    images = models.ManyToManyField(
        "HotelImage",
        verbose_name='Фотографии отеля',
        related_name='hotels',
        blank=True
    )
    amenities = models.ManyToManyField(
        "Amenity",
        verbose_name='Удобства отеля',
        related_name='hotels',
        blank=True
    )

    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'

    def __str__(self):
        return self.name


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name='Отель', related_name='room_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=60, verbose_name='Название типа номера')
    description = models.TextField(blank=True, null=True, verbose_name='Описание типа номера')
    occupancy = models.PositiveIntegerField(verbose_name='Максимальное количество гостей')
    amenities = models.ManyToManyField("Amenity", verbose_name='Удобства типа номера', related_name='room_types', blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за ночь', default=0.00)

    class Meta:
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типы номеров'
        unique_together = ['hotel', 'name']
    def __str__(self):
        return f"{self.hotel.name} - {self.name}"



class Room(models.Model):
    room_type = models.ForeignKey(RoomType, verbose_name='Тип номера', related_name='rooms', on_delete=models.CASCADE)
    number = models.CharField(max_length=10, verbose_name='Номер комнаты')
    preview = models.ImageField(null=True, blank=True,
                                upload_to=room_preview_directory_path,
                                verbose_name='Главное фото номера')
    images = models.ManyToManyField(
        "RoomImage",
        verbose_name='Фотографии номера',
        related_name='rooms',
        blank=True
    )

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'
        unique_together = ['room_type', 'number']


    def __str__(self):
        return f"{self.room_type.hotel.name} - {self.room_type.name} - {self.number}"


class Amenity(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название удобства', unique=True)

    class Meta:
        verbose_name = 'Удобство'
        verbose_name_plural = 'Удобства'

    def __str__(self):
        return self.name


class HotelImage(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        verbose_name='Отель',
        related_name='hotel_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=hotel_photo_directory_path, verbose_name='Фотография отеля')

    class Meta:
        verbose_name = 'Фотография отеля'
        verbose_name_plural = 'Фотографии отеля'

    def __str__(self):
        return f"Фотография для {self.hotel.name}"


class RoomImage(models.Model):
    room = models.ForeignKey(
        Room,
        verbose_name='Номер',
        related_name='room_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=room_photo_directory_path, verbose_name='Фотография номера')

    class Meta:
        verbose_name = 'Фотография номера'
        verbose_name_plural = 'Фотографии номера'

    def __str__(self):
        return f"Фотография для номера {self.room.number}"


class Review(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name='Отель', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['hotel', 'user']

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.hotel.name}"