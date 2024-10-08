from django.urls import path
from ventas import views

urlpatterns=[
    path('gestventas/',views.ventas, name='ventas'),
    path('addventa/',views.add_venta, name='addventa'),
    path('consventa/',views.cons_venta, name='consventa'),
 ]