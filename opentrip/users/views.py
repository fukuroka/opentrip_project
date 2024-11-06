from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import CustomLoginForm, CustomerRegisterForm, HotelRegisterForm
from users.models import CustomerProfile,HotelProfile, User

class CustomLoginView(LoginView):
    template_name = 'users/customer_profile.html'
    authentication_form = CustomLoginForm
    success_url = reverse_lazy('main')


class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegisterForm
    template_name = 'users/customer_register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        customer_profile, created = CustomerProfile.objects.get_or_create(user=user)

        customer_profile.name = form.cleaned_data['first_name']
        customer_profile.surname = form.cleaned_data['last_name']
        customer_profile.phone_number = form.cleaned_data['phone_number']

        customer_profile.save()

        return super().form_valid(form)

class HotelRegisterView(CreateView):
    model = User
    form_class = HotelRegisterForm
    template_name = 'users/hotel_register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save(commit=False)

        user.user_type = 'hotel'

        user.save()

        hotel_profile, created = HotelProfile.objects.get_or_create(user=user)

        hotel_profile.phone_number = form.cleaned_data['phone_number']
        hotel_profile.website = form.cleaned_data['website']

        hotel_profile.save()

        return super().form_valid(form)