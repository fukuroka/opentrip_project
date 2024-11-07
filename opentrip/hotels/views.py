from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from hotels.models import Hotel, RoomType, HotelImage
from datetime import datetime
from hotels.filters import RoomTypeFilter
from hotels.forms import HotelForm


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


class HotelRoomTypesView(DetailView):
    model = Hotel
    template_name = 'hotels/types_room_list.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        check_in_str = self.request.GET.get('check_in')
        check_out_str = self.request.GET.get('check_out')
        nights = None

        if check_in_str and check_out_str:
            try:
                check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
                check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
                nights = (check_out - check_in).days
            except ValueError:
                pass

        context['room_types'] = RoomType.objects.filter(hotel=self.object).order_by('-price_per_night').prefetch_related('amenities', 'images')
        filter = RoomTypeFilter(self.request.GET, queryset=context['room_types'])
        context['filter'] = filter
        context['nights'] = nights
        context['check_in'] = check_in
        context['check_out'] = check_out

        for room_type in filter.qs:
            if nights is not None:
                room_type.price_selected_nights = room_type.price_per_night * nights
            else:
                room_type.price_selected_nights = None

            print(f"Цена за {nights} ночей для {room_type.name}: {room_type.price_selected_nights}")

        return context

class HotelCreateView(LoginRequiredMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'hotels/create_hotel.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        hotel = form.save(commit=False)
        hotel.user = self.request.user
        hotel.save()

        return super().form_valid(form)
