from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_parking_spots, name='list_parking_spots'),
    path('adicionar/', views.add_parking_spot, name='add_parking_spot'),
    path('assinaturas/', views.list_subscriptions, name='list_subscriptions'),
    path('assinaturas/adicionar/', views.add_subscription, name='add_subscription'),
    path('assinaturas/<int:pk>/editar/', views.edit_subscription, name='edit_subscription'),
    path('assinaturas/<int:pk>/excluir/', views.delete_subscription, name='delete_subscription'),
    path('<int:pk>/editar/', views.edit_parking_spot, name='edit_parking_spot'),
    path('<int:pk>/excluir/', views.delete_parking_spot, name='delete_parking_spot'),
]
