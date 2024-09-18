from django.urls import path
from clientes import views

urlpatterns=[
    path('admclientes/', views.clientes , name='clientes'),
    path('addcliente/',views.add_cliente, name='addcliente'),
    path('modcliente/<int:cliente_id>/', views.mod_cliente, name='modcliente'),
    path('delcliente/<int:cliente_id>/', views.del_cliente, name='delcliente'),
]