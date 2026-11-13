
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class CustomLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.role == CustomUser.Role.ADMIN:
            return reverse("admin_panel")

        return reverse("dashboard")
