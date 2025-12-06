from django.urls import path
from . import views

app_name = 'pasajeros'

urlpatterns = [
    # API para React
    path('api/pasajeros/', views.crear_pasajero_api, name='api_crear_pasajero'),
]