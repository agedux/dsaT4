from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import re

class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField(
        required=True,
        min_value=13,
        help_text='Must be 13 years or older'
    )    
    class Meta:
        model = User
        fields = ("username", "age", "password1", "password2")
        
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characterslong.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must include at least one number.")
        if not re.search(r'[^\w\d\s]', password):
            raise forms.ValidationError("Password must include at least one special character.")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                age=self.cleaned_data['age']
            )
        return user