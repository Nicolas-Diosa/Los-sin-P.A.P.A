# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # Agrega el campo email
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        required=True, # Hazlo obligatorio
        help_text='Obligatorio. Ingresa una dirección de correo válida.',
    )

    class Meta:
        # Hereda los campos de UserCreationForm, y agrega 'email'
        model = User
        fields = ("username", "email") + UserCreationForm.Meta.fields[2:]