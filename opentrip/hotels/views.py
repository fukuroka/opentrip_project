from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from hotels.models import Hotel
from bookings.models import BookedRoom
from datetime import datetime



class MainView(TemplateView):
    template_name = 'hotels/main.html'

class SearchHotelsView(ListView):
    template_name = 'hotels/search_hotels.html'
    model = Hotel
    context_object_name = 'hotels'

    city_glob = ''
    nights = 0
    price_selected_nights = 0


    def get_queryset(self):
        queryset = super().get_queryset()
        city = self.request.GET.get('city')
        check_in = datetime.strptime(self.request.GET.get('check_in'),'%Y-%m-%d').date()
        check_out = datetime.strptime(self.request.GET.get('check_out'),'%Y-%m-%d').date()
        self.city_glob = city
        self.nights = int((check_out - check_in).days)

        if city:
            queryset = queryset.filter(city = city)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchHotelsView,self).get_context_data(**kwargs)
        context['city'] = self.city_glob
        context['nights'] = self.nights

        for hotel in context['hotels']:
            cheapest_room_type = hotel.room_types.order_by('price_per_night').first()
            hotel.cheapest_room_type = cheapest_room_type
            hotel.price_selected_nights = cheapest_room_type.price_per_night * context['nights']

        return context
