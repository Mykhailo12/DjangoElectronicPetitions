from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Petition

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'father', 'password1', 'password2']

class PetitionForm(ModelForm):
    class Meta:
        model = Petition
        fields = '__all__'
        exclude = ['author', 'subs']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
