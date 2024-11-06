from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from hotels.models import Hotel
from django.core.validators import RegexValidator


def user_avatar_directory_path(instance, filename):
    return f'users/avatars/{instance.user.username}/{filename}'


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Обычный пользователь'),
        ('hotel', 'Отель'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name='Тип пользователя'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class HotelProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='hotel_profile',
        limit_choices_to={'user_type': 'hotel'},
        verbose_name='Пользователь (отель)'
    )
    hotel = models.OneToOneField(
        Hotel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Отель',
        related_name='hotel_profile'
    )
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Номер телефона')
    website = models.URLField(blank=True, verbose_name='Веб-сайт')

    class Meta:
        verbose_name = 'Профиль отеля'
        verbose_name_plural = 'Профили отелей'

    def __str__(self):
        return self.user.username if not self.hotel else self.hotel.name

    def save(self, *args, **kwargs):
        if self._state.adding and self.hotel:
            self.user.username = self.hotel.name
            self.user.save()
        super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        limit_choices_to={'user_type': 'customer'},
        verbose_name='Пользователь (клиент)'
    )
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    birthdate = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to=user_avatar_directory_path, blank=True, null=True, verbose_name='Аватар пользователя')


    class Meta:
        verbose_name = 'Профиль клиента'
        verbose_name_plural = 'Профили клиентов'

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.user.first_name = self.name
            self.user.last_name = self.surname
            self.user.save()
        else:
            orig = CustomerProfile.objects.get(pk=self.pk)
            if orig.name != self.name:
                self.user.first_name = self.name
            if orig.surname != self.surname:
                self.user.last_name = self.surname
            self.user.save()

        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'hotel':
            HotelProfile.objects.create(user=instance)
        elif instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)


def get_user_profile(user):
    if user.user_type == "customer":
        return user.customer_profile
    elif user.user_type == "hotel":
        return user.hotel_profile
    return None