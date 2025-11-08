from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Pasaje, AsientoViaje
from .utils import generar_ticket_pdf
import json
from datetime import datetime


@login_required
def descargar_ticket(request, pasaje_id):
    """Descarga el ticket en PDF"""
    pasaje = get_object_or_404(Pasaje, id=pasaje_id)
    
    pdf = generar_ticket_pdf(pasaje)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{pasaje.codigo_ticket}.pdf"'
    
    return response


# ========================================
# NUEVAS VISTAS PARA SELECCIÓN DE ASIENTOS
# ========================================

@login_required
def seleccionar_asiento_view(request):
    """
    Vista para mostrar la interfaz de selección de asientos
    """
    # Obtener parámetros del viaje desde la URL
    fecha_viaje = request.GET.get('fecha_viaje')
    hora_salida = request.GET.get('hora_salida')
    origen = request.GET.get('origen', 'Lima')
    destino = request.GET.get('destino', 'Ferreñafe')
    tipo_servicio = request.GET.get('tipo_servicio', 'economico')
    precio = request.GET.get('precio', '0.00')
    
    # ID del pasajero si viene de un flujo de venta
    pasajero_id = request.GET.get('pasajero_id')
    
    context = {
        'fecha_viaje': fecha_viaje,
        'hora_salida': hora_salida,
        'origen': origen,
        'destino': destino,
        'tipo_servicio': tipo_servicio,
        'precio': precio,
        'pasajero_id': pasajero_id,
    }
    
    return render(request, 'pasajes/seleccionar_asiento.html', context)

@login_required
@require_http_methods(["GET"])
def obtener_asientos_api(request):
    """
    API para obtener el estado de los asientos en tiempo real
    Retorna JSON con los asientos disponibles y ocupados
    """
    fecha_viaje = request.GET.get('fecha_viaje')
    hora_salida = request.GET.get('hora_salida')
    origen = request.GET.get('origen', 'Lima')
    destino = request.GET.get('destino', 'Ferreñafe')
    
    # Validar parámetros
    if not fecha_viaje or not hora_salida:
        return JsonResponse({
            'success': False,
            'error': 'Faltan parámetros: fecha_viaje y hora_salida son requeridos'
        }, status=400)
    
    # Convertir fecha string a objeto date
    try:
        fecha_obj = datetime.strptime(fecha_viaje, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
        }, status=400)
    
    # PRIMERO verificar si existen asientos para este viaje
    asientos_existentes = AsientoViaje.objects.filter(
        fecha_viaje=fecha_obj,
        hora_salida=hora_salida,
        origen=origen,
        destino=destino
    ).exists()
    
    # SOLO inicializar si NO existen
    if not asientos_existentes:
        AsientoViaje.inicializar_asientos_viaje(
            fecha_obj, hora_salida, origen, destino
        )
    
    # Obtener todos los asientos
    asientos = AsientoViaje.objects.filter(
        fecha_viaje=fecha_obj,
        hora_salida=hora_salida,
        origen=origen,
        destino=destino
    ).order_by('piso', 'numero_asiento')
    
    # Separar por pisos
    asientos_piso1 = []
    asientos_piso2 = []
    
    for asiento in asientos:
        asiento_data = {
            'id': asiento.pk,
            'numero': asiento.numero_asiento,
            'ocupado': asiento.ocupado,
            'piso': asiento.piso
        }
        
        if asiento.piso == 1:
            asientos_piso1.append(asiento_data)
        else:
            asientos_piso2.append(asiento_data)
    
    total_disponibles = asientos.filter(ocupado=False).count()
    total_ocupados = asientos.filter(ocupado=True).count()
    
    return JsonResponse({
        'success': True,
        'piso1': asientos_piso1,
        'piso2': asientos_piso2,
        'total_disponibles': total_disponibles,
        'total_ocupados': total_ocupados
    })


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def reservar_asiento_api(request):
    """
    API para reservar temporalmente un asiento
    Marca el asiento como ocupado hasta que se confirme o cancele
    """
    try:
        data = json.loads(request.body)
        asiento_id = data.get('asiento_id')
        
        if not asiento_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del asiento es requerido'
            }, status=400)
        
        # Obtener el asiento (usar pk en lugar de id)
        asiento = get_object_or_404(AsientoViaje, pk=asiento_id)
        
        # Verificar que no esté ocupado
        if asiento.ocupado:
            return JsonResponse({
                'success': False,
                'error': 'El asiento ya está ocupado por otro pasajero'
            }, status=409)  # 409 Conflict
        
        # Marcar como ocupado temporalmente
        asiento.ocupado = True
        asiento.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Asiento {asiento.numero_asiento} reservado exitosamente',
            'asiento_numero': asiento.numero_asiento,
            'asiento_piso': asiento.piso,
            'asiento_id': asiento.pk
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido en el cuerpo de la solicitud'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def liberar_asiento_api(request):
    """
    API para liberar un asiento previamente reservado
    Se usa cuando el usuario cambia de asiento o cancela la selección
    """
    try:
        data = json.loads(request.body)
        asiento_id = data.get('asiento_id')
        
        if not asiento_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del asiento es requerido'
            }, status=400)
        
        # Obtener el asiento (usar pk en lugar de id)
        asiento = get_object_or_404(AsientoViaje, pk=asiento_id)
        
        # Liberar asiento solo si no tiene un pasaje asociado
        # (Si tiene pasaje, significa que ya se confirmó la venta)
        if asiento.pasaje is None:
            asiento.ocupado = False
            asiento.save()
            
            return JsonResponse({
                'success': True,
                'mensaje': f'Asiento {asiento.numero_asiento} liberado exitosamente'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No se puede liberar un asiento con pasaje confirmado'
            }, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido en el cuerpo de la solicitud'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["GET"])
def verificar_asiento_api(request):
    """
    API para verificar si un asiento específico está disponible
    Útil antes de proceder con la venta
    """
    fecha_viaje = request.GET.get('fecha_viaje')
    hora_salida = request.GET.get('hora_salida')
    origen = request.GET.get('origen', 'Lima')
    destino = request.GET.get('destino', 'Ferreñafe')
    numero_asiento = request.GET.get('numero_asiento')
    
    if not all([fecha_viaje, hora_salida, numero_asiento]):
        return JsonResponse({
            'success': False,
            'error': 'Faltan parámetros requeridos'
        }, status=400)
    
    try:
        fecha_obj = datetime.strptime(fecha_viaje, '%Y-%m-%d').date()
        numero_asiento = int(numero_asiento)
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'error': 'Parámetros inválidos'
        }, status=400)
    
    # Verificar disponibilidad
    disponible = AsientoViaje.verificar_disponibilidad(
        fecha_obj, hora_salida, origen, destino, numero_asiento
    )
    
    return JsonResponse({
        'success': True,
        'disponible': disponible,
        'numero_asiento': numero_asiento
    })