from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('on-consideration/', views.consideration, name='consideration'),
    path('petition/<str:pk>/', views.petitionDetail, name='petition-detail'),

    path('create-petition/', views.createPetition, name='petition-create'),
    path('update-petition/<str:pk>/', views.updatePetition, name='petition-update'),
    path('delete-petition/<str:pk>/', views.deletePetition, name='petition-delete'),

    path('subscribe/<str:pk>/', views.subscribe, name='subscribe'),

    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
]
