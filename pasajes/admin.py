from django.contrib import admin
from django.utils.html import format_html
from .models import Pasaje, AsientoViaje, ConfiguracionBus


@admin.register(Pasaje)
class PasajeAdmin(admin.ModelAdmin):
    list_display = ['codigo_ticket', 'pasajero', 'fecha_viaje', 'hora_salida', 'numero_asiento', 'estado', 'total_pagar', 'vendedor', 'descargar_ticket_link']
    search_fields = ['codigo_ticket', 'pasajero__dni', 'pasajero__nombres', 'pasajero__apellidos']
    list_filter = ['estado', 'fecha_viaje', 'tipo_servicio', 'lleva_equipaje', 'lleva_encomienda']
    readonly_fields = ['codigo_ticket', 'fecha_venta', 'fecha_actualizacion', 'numero_ediciones', 'descargar_ticket_button', 'seleccionar_asiento_button']
    
    fieldsets = (
        ('Pasajero', {
            'fields': ('pasajero',)
        }),
        ('Viaje', {
            'fields': ('fecha_viaje', 'hora_salida', 'origen', 'destino', 'seleccionar_asiento_button', 'numero_asiento', 'tipo_servicio')
        }),
        ('Precio', {
            'fields': ('precio', 'cargo_adicional')
        }),
        ('Equipaje y Encomiendas', {
            'fields': ('lleva_equipaje', 'cantidad_maletas', 'lleva_encomienda', 'descripcion_encomienda', 'peso_encomienda'),
            'classes': ('collapse',)
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
    
    @admin.display(description='Selección Visual')
    def seleccionar_asiento_button(self, obj):
        """Botón para abrir la interfaz de selección visual de asientos"""
        return format_html(
            '''
            <div style="margin: 15px 0;">
                <button type="button" onclick="abrirSelectorAsientos()" class="button"
                   style="padding: 12px 20px; 
                          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; 
                          border: none;
                          border-radius: 8px; 
                          font-weight: bold;
                          cursor: pointer;
                          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                    🎫 Seleccionar Asiento Visual
                </button>
                <p style="margin-top: 10px; color: #666; font-size: 12px;">
                    📋 Primero completa: Fecha de Viaje, Hora de Salida, Origen y Destino. 
                    Luego haz clic aquí para seleccionar el asiento visualmente.
                </p>
            </div>
            <script>
            function abrirSelectorAsientos() {{
                var fechaViaje = document.getElementById('id_fecha_viaje').value;
                var horaSalida = document.getElementById('id_hora_salida').value;
                var origen = document.getElementById('id_origen').value;
                var destino = document.getElementById('id_destino').value;
                var tipoServicio = document.getElementById('id_tipo_servicio').value;
                var precio = document.getElementById('id_precio').value || '50.00';
                
                // Validar solo campos esenciales (sin precio)
                var camposFaltantes = [];
                if (!fechaViaje) camposFaltantes.push('Fecha de Viaje');
                if (!horaSalida) camposFaltantes.push('Hora de Salida');
                if (!origen) camposFaltantes.push('Origen');
                if (!destino) camposFaltantes.push('Destino');
                if (!tipoServicio) camposFaltantes.push('Tipo de Servicio');
                
                if (camposFaltantes.length > 0) {{
                    alert('⚠️ Por favor completa los siguientes campos:\\n\\n' + camposFaltantes.join('\\n'));
                    return false;
                }}
                
                // Convertir fecha de DD/MM/YYYY a YYYY-MM-DD
                var fechaConvertida = fechaViaje;
                if (fechaViaje.includes('/')) {{
                    var partes = fechaViaje.split('/');
                    if (partes.length === 3) {{
                        fechaConvertida = partes[2] + '-' + partes[1] + '-' + partes[0];
                    }}
                }}
                
                var url = '/pasajes/seleccionar-asiento/?' + 
                          'fecha_viaje=' + encodeURIComponent(fechaConvertida) +
                          '&hora_salida=' + encodeURIComponent(horaSalida) +
                          '&origen=' + encodeURIComponent(origen) +
                          '&destino=' + encodeURIComponent(destino) +
                          '&tipo_servicio=' + encodeURIComponent(tipoServicio) +
                          '&precio=' + encodeURIComponent(precio);
                
                window.open(url, 'SeleccionAsiento', 'width=1200,height=800');
            }}
            
            window.addEventListener('message', function(event) {{
                if (event.data && event.data.asientoSeleccionado) {{
                    document.getElementById('id_numero_asiento').value = event.data.asientoSeleccionado;
                    document.getElementById('id_numero_asiento').style.backgroundColor = '#d4edda';
                    alert('✅ Asiento ' + event.data.asientoSeleccionado + ' seleccionado correctamente');
                }}
            }});
            </script>
            '''
        )
    
    @admin.display(description='Descargar Ticket')
    def descargar_ticket_button(self, obj):
        """Botón para descargar ticket en PDF"""
        if obj.pk:
            return format_html(
                '<a class="button" href="/pasajes/{}/ticket/" target="_blank" style="padding: 10px 15px; background: #417690; color: white; text-decoration: none; border-radius: 4px;">📄 Descargar Ticket PDF</a>',
                obj.pk
            )
        return "Guarda primero para generar el ticket"
    
    @admin.display(description='Ticket')
    def descargar_ticket_link(self, obj):
        """Link a ticket en la lista"""
        if obj.pk:
            return format_html(
                '<a href="/pasajes/{}/ticket/" target="_blank">PDF</a>',
                obj.pk
            )
        return "-"
    
# def response_add(self, request, obj, post_url_continue=None):
#     """Asociar el asiento al pasaje al guardar"""
#     if obj.pk:
#         try:
#             asiento = AsientoViaje.objects.get(
#                 fecha_viaje=obj.fecha_viaje,
#                 hora_salida=obj.hora_salida,
#                 origen=obj.origen,
#                 destino=obj.destino,
#                 numero_asiento=obj.numero_asiento
#             )
#             asiento.pasaje = obj
#             asiento.ocupado = True
#             asiento.save()
#         except AsientoViaje.DoesNotExist:
#             pass
#     
#     return super().response_add(request, obj, post_url_continue)


@admin.register(AsientoViaje)
class AsientoViajeAdmin(admin.ModelAdmin):
    list_display = ['numero_asiento', 'piso', 'fecha_viaje', 'hora_salida', 'origen', 'destino', 'estado_ocupado', 'pasaje_asociado']
    list_filter = ['ocupado', 'piso', 'fecha_viaje', 'origen', 'destino']
    search_fields = ['numero_asiento', 'fecha_viaje']
    readonly_fields = ['fecha_reserva', 'ultima_actualizacion']
    
    fieldsets = (
        ('Información del Viaje', {
            'fields': ('fecha_viaje', 'hora_salida', 'origen', 'destino')
        }),
        ('Información del Asiento', {
            'fields': ('numero_asiento', 'piso', 'ocupado', 'pasaje')
        }),
        ('Auditoría', {
            'fields': ('fecha_reserva', 'ultima_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Estado')
    def estado_ocupado(self, obj):
        """Mostrar estado visual del asiento"""
        if obj.ocupado:
            return format_html(
                '<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px; font-weight: bold;">🔴 OCUPADO</span>'
            )
        return format_html(
            '<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px; font-weight: bold;">🟢 DISPONIBLE</span>'
        )
    
    @admin.display(description='Pasaje')
    def pasaje_asociado(self, obj):
        """Link al pasaje asociado"""
        if obj.pasaje:
            return format_html(
                '<a href="/admin/pasajes/pasaje/{}/change/">{}</a>',
                obj.pasaje.pk,
                obj.pasaje.codigo_ticket
            )
        return "-"


@admin.register(ConfiguracionBus)
class ConfiguracionBusAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_servicio_display', 'pisos', 'total_asientos', 'activo']
    list_filter = ['tipo_servicio', 'pisos', 'activo']
    search_fields = ['nombre']
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'tipo_servicio', 'activo')
        }),
        ('Configuración de Asientos', {
            'fields': ('pisos', 'total_asientos', 'asientos_piso1', 'asientos_piso2')
        }),
    )
    
    @admin.display(description='Tipo de Servicio')
    def tipo_servicio_display(self, obj):
        """Mostrar tipo de servicio formateado"""
        tipos = {
            'economico': 'Económico',
            'vip': 'VIP',
            'cama': 'Semi Cama',
            'suite': 'Suite',
        }
        return tipos.get(obj.tipo_servicio, obj.tipo_servicio)