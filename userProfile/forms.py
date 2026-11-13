
from django import forms
from accounts.models import CustomUser


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "course",
            "contact_number",
            "profile_picture",
        ]
