from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('diario/', views.reporte_diario, name='reporte_diario'),
    path('mensual/', views.reporte_mensual, name='reporte_mensual'),
    path('anual/', views.reporte_anual, name='reporte_anual'),
]