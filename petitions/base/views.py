from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Petition, User, Topic
from .forms import MyUserCreationForm, PetitionForm

def home(request):
    pets = Petition.objects.all()
    context = {'pets':pets}
    return render(request, 'base/home.html', context)

def petitionDetail(request, pk):
    pet = Petition.objects.get(id=pk)
    context = {'pet': pet}
    return render(request, 'base/petition-detail.html', context)

@login_required(login_url='login')
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            print("nashli")
        except:
            print('pizda')
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('pobeda')
            login(request, user)
            return redirect('home')
        else:
            HttpResponse('fail.')

    context = {'page':page}
    return render(request, 'base/login-register.html', context)

@login_required(login_url='login')
def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error ocured during registration')

    return render(request, 'base/login-register.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def createPetition(request):
    form = PetitionForm()
    topic = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Petition.objects.create(
            author=request.user,
            topic=topic,
            name=request.POST.get('name'),
        )
        return redirect('home')


    context = {'form':form, 'topic':topic}
    return render(request, 'base/petition-form.html', context)

@login_required(login_url='login')
def updatePetition(request, pk):
    pet = Petition.objects.get(id=pk)
    form = PetitionForm(instance=pet)
    topics = Topic.objects.all()

    if request.user != pet.author:
        return HttpResponse("Your are not allowed here!!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        pet.name = request.POST.get('name')
        pet.topic = topic
        pet.description = request.POST.get('description')
        pet.save()
        return redirect('home')

    context = {'form':form, 'topics':topics, 'pet':pet}
    return render(request, 'base/petition-form.html', context)

@login_required(login_url='login')
def deletePetition(request, pk):
    pet = Petition.objects.get(id=pk)
    if request.method == 'POST':
        pet.delete()
        return redirect('home')
    return render(request, 'base/petition-delete.html', {'obj':pet})

