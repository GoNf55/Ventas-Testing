from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.productos, name='productos'),
    path('addproducto/', views.addproductos, name='addproducto'),
    path('modproducto/<int:producto_id>/', views.modproductos, name='modproducto'),
]