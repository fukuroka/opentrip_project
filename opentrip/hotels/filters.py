import django_filters
from .models import RoomType

class RoomTypeFilter(django_filters.FilterSet):
    occupancy = django_filters.NumberFilter(field_name='occupancy', lookup_expr='gte', label='Количество гостей')

    class Meta:
        model = RoomType
        fields = ['occupancy']