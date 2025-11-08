from django.urls import path
from . import views

app_name = 'pasajes'

urlpatterns = [
    # Ruta original - Descargar ticket
    path('<int:pasaje_id>/ticket/', views.descargar_ticket, name='descargar_ticket'),
    
    # ========================================
    # NUEVAS RUTAS - SISTEMA DE SELECCIÓN DE ASIENTOS
    # ========================================
    
    # Vista principal de selección de asientos
    path('seleccionar-asiento/', views.seleccionar_asiento_view, name='seleccionar_asiento'),
    
    # APIs para manejo de asientos en tiempo real
    path('api/asientos/', views.obtener_asientos_api, name='obtener_asientos'),
    path('api/reservar-asiento/', views.reservar_asiento_api, name='reservar_asiento'),
    path('api/liberar-asiento/', views.liberar_asiento_api, name='liberar_asiento'),
    path('api/verificar-asiento/', views.verificar_asiento_api, name='verificar_asiento'),
]