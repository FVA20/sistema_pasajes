from django.contrib import admin
from .models import Pasajero


@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ['dni', 'nombre_completo', 'telefono', 'fecha_nacimiento', 'edad', 'fecha_registro']
    search_fields = ['dni', 'nombres', 'apellidos', 'telefono']
    list_filter = ['fecha_registro', 'activo']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'dni', 'fecha_nacimiento')
        }),
        ('Contacto', {
            'fields': ('telefono', 'correo')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_registro', 'fecha_actualizacion')
        }),
    )