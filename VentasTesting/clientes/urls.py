from django.urls import path
from clientes import views

urlpatterns=[
    path('admclientes/', views.clientes , name='clientes'),
]