from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition, User, Topic
from .forms import MyUserCreationForm, PetitionForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    pets = Petition.objects.filter(Q(name__icontains=q))

    context = {'pets':pets}
    return render(request, 'base/home.html', context)

def consideration(request):
    pets = Petition.objects.all()

    context = {'pets': pets}
    return render(request, 'base/on-consideration.html', context)

def petitionDetail(request, pk):
    pet = Petition.objects.get(id=pk)
    context = {'pet': pet}
    return render(request, 'base/petition-detail.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
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

def check_petitions(pet):
    pet_subs_count =  pet.subs.count()
    print(pet_subs_count)
    if pet_subs_count >= 10:
        pet.status = "На розгляді"
        pet.save()
        return pet

def subscribe(request, pk):
    pet = Petition.objects.get(id=pk)
    if request.user != pet.author:
        pet.subs.add(request.user)
        check_petitions(pet)
        return redirect('home')
    else:
        return HttpResponse("Your are not allowed here!!")

@login_required(login_url='login')
def createPetition(request):
    form = PetitionForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic = get_object_or_404(Topic, id=topic_name)

        Petition.objects.create(
            author=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')


    context = {'form':form, 'topics':topics}
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

