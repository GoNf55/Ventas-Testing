from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.productos, name='productos'),
    path('addproducto/', views.addproductos, name='addproducto'),
    path('modproducto/<int:producto_id>/', views.modproductos, name='modproducto'),
    path('delproducto/<int:producto_id>/', views.delproductos, name='delprodcuto'),
    path('categorias/', views.categorias, name='categorias'),
    path('addcategorias/',views.addcategorias, name='addcategorias'),
    path('modcategorias/<int:categoria_id>/', views.modcategorias, name='modcategorias'),
    path('delcategorias/<int:categoria_id>/', views.delcategorias, name='delcategorias')
]