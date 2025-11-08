// static/admin/js/seleccion_asiento.js

(function($) {
    $(document).ready(function() {
        // Capturar el click en el botón de seleccionar asiento
        $(document).on('click', 'a[href*="seleccionar-asiento"]', function(e) {
            e.preventDefault();
            
            // Obtener valores de los campos del formulario
            var fechaViaje = $('#id_fecha_viaje').val();
            var horaSalida = $('#id_hora_salida').val();
            var origen = $('#id_origen').val();
            var destino = $('#id_destino').val();
            var tipoServicio = $('#id_tipo_servicio').val();
            var precio = $('#id_precio').val();
            
            // Validar que los campos estén llenos
            var camposFaltantes = [];
            if (!fechaViaje) camposFaltantes.push('Fecha de Viaje');
            if (!horaSalida) camposFaltantes.push('Hora de Salida');
            if (!origen) camposFaltantes.push('Origen');
            if (!destino) camposFaltantes.push('Destino');
            if (!tipoServicio) camposFaltantes.push('Tipo de Servicio');
            if (!precio) camposFaltantes.push('Precio');
            
            if (camposFaltantes.length > 0) {
                alert('⚠️ Por favor completa los siguientes campos antes de seleccionar el asiento:\n\n' + camposFaltantes.join('\n'));
                return false;
            }
            
            // Construir URL con parámetros
            var url = '/pasajes/seleccionar-asiento/?' + 
                      'fecha_viaje=' + encodeURIComponent(fechaViaje) +
                      '&hora_salida=' + encodeURIComponent(horaSalida) +
                      '&origen=' + encodeURIComponent(origen) +
                      '&destino=' + encodeURIComponent(destino) +
                      '&tipo_servicio=' + encodeURIComponent(tipoServicio) +
                      '&precio=' + encodeURIComponent(precio);
            
            // Abrir en nueva ventana
            var ventana = window.open(url, 'SeleccionAsiento', 'width=1200,height=800,scrollbars=yes');
            
            if (!ventana) {
                alert('⚠️ Por favor, permite las ventanas emergentes para este sitio.');
            }
            
            return false;
        });
        
        // Escuchar mensajes de la ventana de selección de asientos
        window.addEventListener('message', function(event) {
            if (event.data && event.data.asientoSeleccionado) {
                // Rellenar el campo de número de asiento
                $('#id_numero_asiento').val(event.data.asientoSeleccionado);
                
                // Marcar visualmente que se seleccionó
                $('#id_numero_asiento').css('background-color', '#d4edda');
                
                // Mostrar mensaje de éxito
                alert('✅ Asiento ' + event.data.asientoSeleccionado + ' seleccionado correctamente');
            }
        });
    });
})(django.jQuery);