from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import Petition
from .forms import LoginForm

def home(request):
    pets = Petition.objects.all()
    context = {'pets':pets}
    return render(request, 'base/home.html', context)

def petitionDetail(request, pk):
    pet = Petition.objects.get(id=pk)
    context = {'pet': pet}
    return render(request, 'base/petition-detail.html', context)

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    context = {'page':page, 'form': form}
    return render(request, 'base/login-register.html', context)