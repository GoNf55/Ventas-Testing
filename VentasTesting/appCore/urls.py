from django.urls import path
from appCore import views

urlpatterns=[
    path('', views.home,  name='home'),
    path('deslogueo/', views.deslogueo, name='deslogueo'),
    path('registro/', views.registro, name='registro')
]