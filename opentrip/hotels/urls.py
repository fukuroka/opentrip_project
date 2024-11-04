from django.urls import path
from .views import SearchHotelsView

app_name = 'hotels_app'

urlpatterns = [
    path('hotels/', SearchHotelsView.as_view(), name = 'search_hotels')
]
