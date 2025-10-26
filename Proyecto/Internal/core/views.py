from django.shortcuts import render
from django.http import HttpResponse
from core.Negocio.auth import *
from .forms import CustomUserCreationForm

# Create your views here.

def view_register(request):
    if request.method == 'GET':
        return render(request, 'core/register.html', {
            'form': CustomUserCreationForm
        })
    else:
        return auth.register_user(request=request)
def home(request):
    return render(request, 'core/home.html')