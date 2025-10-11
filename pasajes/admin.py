from django.contrib import admin
from django.utils.html import format_html
from .models import Pasaje


@admin.register(Pasaje)
class PasajeAdmin(admin.ModelAdmin):
    list_display = ['codigo_ticket', 'pasajero', 'fecha_viaje', 'hora_salida', 'numero_asiento', 'estado', 'total_pagar', 'vendedor', 'descargar_ticket_link']
    search_fields = ['codigo_ticket', 'pasajero__dni', 'pasajero__nombres', 'pasajero__apellidos']
    list_filter = ['estado', 'fecha_viaje', 'tipo_servicio', 'lleva_equipaje', 'lleva_encomienda']
    readonly_fields = ['codigo_ticket', 'fecha_venta', 'fecha_actualizacion', 'numero_ediciones', 'descargar_ticket_button']
    
    fieldsets = (
        ('Pasajero', {
            'fields': ('pasajero',)
        }),
        ('Viaje', {
            'fields': ('fecha_viaje', 'hora_salida', 'origen', 'destino', 'numero_asiento', 'tipo_servicio')
        }),
        ('Precio', {
            'fields': ('precio', 'cargo_adicional')
        }),
        ('Equipaje y Encomiendas', {
            'fields': ('lleva_equipaje', 'cantidad_maletas', 'lleva_encomienda', 'descripcion_encomienda', 'peso_encomienda')
        }),
        ('Estado', {
            'fields': ('estado', 'vendedor', 'numero_ediciones')
        }),
        ('Ticket', {
            'fields': ('descargar_ticket_button',)
        }),
        ('Anulación', {
            'fields': ('fecha_anulacion', 'motivo_anulacion', 'anulado_por', 'monto_reembolso'),
            'classes': ('collapse',)
        }),
        ('Auditoría', {
            'fields': ('codigo_ticket', 'fecha_venta', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.vendedor = request.user
        super().save_model(request, obj, form, change)
    
    def descargar_ticket_button(self, obj):
        if obj.pk:
            return format_html(
                '<a class="button" href="/pasajes/{}/ticket/" target="_blank" style="padding: 10px 15px; background: #417690; color: white; text-decoration: none; border-radius: 4px;">Descargar Ticket PDF</a>',
                obj.pk
            )
        return "Guarda primero para generar el ticket"
    
    def descargar_ticket_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="/pasajes/{}/ticket/" target="_blank">PDF</a>',
                obj.pk
            )
        return "-"