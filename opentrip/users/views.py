from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView
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

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if hasattr(user, 'customer_profile'):
            profile = user.customer_profile
            context.update({
                'is_customer': True,
                'name': profile.name,
                'surname': profile.surname,
                'profile': profile,
                'saved_articles': user.saved_articles.all(),
            })
        elif hasattr(user, 'hotel_profile'):
            profile = user.hotel_profile
            context.update({
                'is_customer': False,
                'phone_number': profile.phone_number,
                'website': profile.website,
                'profile': profile,
            })

        return context


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('main')

class LogoutTemplateView(TemplateView):
    template_name = 'users/logout.html'