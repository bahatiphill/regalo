# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Churches

class CustomChurchCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Churches
        fields = ('username', 'email', 'location', 'umushumba' )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Churches
        fields = ('username', 'email' , 'location', 'umushumba')