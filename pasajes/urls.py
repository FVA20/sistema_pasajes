from django.urls import path
from . import views

app_name = 'pasajes'

urlpatterns = [
    # APIs REST para React - Ventas
    path('api/asientos/', views.obtener_asientos_api, name='api_obtener_asientos'),
    path('api/pasajes/', views.crear_pasaje_api, name='api_crear_pasaje'),
    path('api/reservar-asiento/', views.reservar_asiento_api, name='api_reservar_asiento'),
    path('api/liberar-asiento/', views.liberar_asiento_api, name='api_liberar_asiento'),
    path('api/verificar-asiento/', views.verificar_asiento_api, name='api_verificar_asiento'),
    
    # APIs REST para React - Administración
    path('api/admin/pasajeros/', views.listar_pasajeros_api, name='api_listar_pasajeros'),
    path('api/admin/editar-pasajero/', views.editar_pasajero_api, name='api_editar_pasajero'),
    path('api/admin/eliminar-pasajero/', views.eliminar_pasajero_api, name='api_eliminar_pasajero'),
    path('api/admin/buscar-dni/', views.buscar_pasajero_por_dni_api, name='api_buscar_dni'),
    path('api/admin/pasajes/', views.listar_pasajes_api, name='api_listar_pasajes'),
    path('api/admin/editar-pasaje/', views.editar_pasaje_api, name='api_editar_pasaje'),
    path('api/admin/eliminar-pasaje/', views.eliminar_pasaje_api, name='api_eliminar_pasaje'),
    path('api/admin/visualizar-asientos/', views.visualizar_asientos_api, name='api_visualizar_asientos'),
    path('api/admin/reporte-diario/', views.reporte_diario_api, name='api_reporte_diario'),
    path('api/admin/reporte-mensual/', views.reporte_mensual_api, name='api_reporte_mensual'),
    path('api/admin/reporte-anual/', views.reporte_anual_api, name='api_reporte_anual'),
    
    # Descargar ticket
    path('api/pasajes/<int:pasaje_id>/ticket/', views.descargar_ticket, name='api_descargar_ticket'),
    path('<int:pasaje_id>/ticket/', views.descargar_ticket, name='descargar_ticket'),
    
    # Vista web
    path('seleccionar-asiento/', views.seleccionar_asiento_view, name='seleccionar_asiento'),
]