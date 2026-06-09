from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('clientes/', include('customers.urls')),
    path('vagas/', include('parking.urls')),
    path('caixa/', include('operations.urls')),
    path('notas/', include('invoices.urls')),
]
