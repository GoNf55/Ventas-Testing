from django.urls import path
from ventas import views

urlpatterns=[
    path('gestventas/',views.ventas, name='ventas'),
    path('addventa/',views.add_venta, name='addventa'),
    path('consventa/<int:venta_id>',views.cons_venta, name='consventa'),
 ]