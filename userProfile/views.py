
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.models import CustomUser
from .forms import ProfileUpdateForm


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "userProfile/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user
