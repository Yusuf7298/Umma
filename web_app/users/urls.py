from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.logout, name="log"),
    path('register/', views.register, name='register'),
]