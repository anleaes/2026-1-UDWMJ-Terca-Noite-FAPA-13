from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_customers, name='list_customers'),
    path('adicionar/', views.add_customer, name='add_customer'),
    path('buscar/', views.search_customers, name='search_customers'),
    path('<int:pk>/editar/', views.edit_customer, name='edit_customer'),
    path('<int:pk>/excluir/', views.delete_customer, name='delete_customer'),
]
