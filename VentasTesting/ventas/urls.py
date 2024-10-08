from django.urls import path
from ventas import views

urlpatterns=[
    path('gestventas/',views.ventas, name='ventas'),
 ]