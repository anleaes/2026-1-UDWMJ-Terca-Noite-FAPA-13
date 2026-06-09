from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_items, name='list_items'),
    path('carrinho/', views.cart, name='cart'),
    path('adicionar/', views.add_to_cart, name='add_to_cart'),
    path('finalizar/', views.checkout, name='checkout'),
]
