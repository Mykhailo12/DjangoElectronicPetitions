from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('petition/<str:pk>/', views.petitionDetail, name='petition-detail'),
    path('login/', views.loginUser, name='login')
]
