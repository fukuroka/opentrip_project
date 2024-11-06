import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

from hotels.models import Room, RoomType
from django.conf import settings


class Booking(models.Model):
    BOOKING_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField(max_length=255, default='111123132')
    surname = models.CharField(max_length=255, default='jdnjfn')
    phone_number = models.CharField(max_length=15,default='1111')
    email = models.EmailField(default='11111')
    booking_reference = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Номер бронирования')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', default=0)
    status = models.CharField(max_length=20, choices=BOOKING_CHOICES, default='pending', verbose_name='Статус')

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f"Бронирование №{self.booking_reference}"

    def calculate_total_price(self):
        total = 0
        for item in self.booked_rooms.all():
            total += item.price
        self.total_price = total
        self.save()


class BookedRoom(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_rooms', verbose_name='Бронирование')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Номер')
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выезда')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)

    class Meta:
        verbose_name = 'Забронированный номер'
        verbose_name_plural = 'Забронированные номера'
        constraints = [
            models.UniqueConstraint(fields=['room', 'check_in'], name='unique_room_booking_date_in'),
        ]

    def __str__(self):
        return f"Номер {self.room.number} ({self.check_in} - {self.check_out})"

    def clean(self):
        overlapping_bookings = BookedRoom.objects.filter(
            room=self.room
        ).exclude(
            Q(check_out__lte=self.check_in) | Q(check_in__gte=self.check_out)
        )

        if overlapping_bookings.exists() and not (self.pk and overlapping_bookings.filter(pk=self.pk).exists()):
            raise ValidationError('Номер уже забронирован на эти даты.')

        if self.check_in >= self.check_out:
            raise ValidationError('Дата выезда должна быть позже даты заезда.')

    def save(self, *args, **kwargs):
        self.clean()
        days = (self.check_out - self.check_in).days
        self.price = self.room.room_type.price_per_night * days
        super().save(*args, **kwargs)
        self.booking.calculate_total_price()


def suggest_alternative_rooms(room_type, check_in, check_out):
    alternative_rooms = Room.objects.filter(
        room_type__hotel=room_type.hotel
    ).exclude(
        id__in=BookedRoom.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)
    )
    return alternative_rooms