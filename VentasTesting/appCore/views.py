from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm

# Create your views here.

@login_required
def home(request):
    return render(request, 'appCore/home.html')

def deslogueo(request):
    logout(request)
    return redirect('home')

def registro(request):
    data={'formulario': CustomUserCreationForm()}

    if request.method == 'POST':
        user_creation_form=CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            return redirect('home')
    return render(request,'registration/register.html', data)
