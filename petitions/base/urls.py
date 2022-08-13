from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('petition/<str:pk>/', views.petitionDetail, name='petition-detail'),

    path('create-petition/', views.createPetition, name='petition-create'),
    path('update-petition/<str:pk>/', views.updatePetition, name='petition-update'),
    path('delete-petition/<str:pk>/', views.deletePetition, name='petition-delete'),

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
]
