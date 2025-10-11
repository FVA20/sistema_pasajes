from django.urls import path
from . import views

app_name = 'pasajes'

urlpatterns = [
    path('<int:pasaje_id>/ticket/', views.descargar_ticket, name='descargar_ticket'),
]