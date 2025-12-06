from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Sum, Count, Q
from .models import Pasaje, AsientoViaje
from .utils import generar_ticket_pdf
import json
from datetime import datetime


# ========================================
# DESCARGA DE TICKET (SIN AUTENTICACIÓN)
# ========================================

def descargar_ticket(request, pasaje_id):
    """Descarga el ticket en PDF"""
    pasaje = get_object_or_404(Pasaje, pk=pasaje_id)
    pdf = generar_ticket_pdf(pasaje)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{pasaje.codigo_ticket}.pdf"'
    return response


# ========================================
# VISTAS CON AUTENTICACIÓN (PARA ADMIN WEB)
# ========================================

@login_required
def seleccionar_asiento_view(request):
    """Vista para mostrar la interfaz de selección de asientos"""
    fecha_viaje = request.GET.get('fecha_viaje')
    hora_salida = request.GET.get('hora_salida')
    origen = request.GET.get('origen', 'Lima')
    destino = request.GET.get('destino', 'Ferreñafe')
    tipo_servicio = request.GET.get('tipo_servicio', 'economico')
    precio = request.GET.get('precio', '0.00')
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


# ========================================
# APIs REST PARA REACT - VENTAS
# ========================================

@csrf_exempt
@require_http_methods(["GET"])
def obtener_asientos_api(request):
    """API para obtener el estado de los asientos en tiempo real"""
    fecha_viaje = request.GET.get('fecha_viaje')
    hora_salida = request.GET.get('hora_salida')
    origen = request.GET.get('origen', 'Lima')
    destino = request.GET.get('destino', 'Ferreñafe')
    
    if not fecha_viaje or not hora_salida:
        return JsonResponse({
            'success': False,
            'error': 'Faltan parámetros: fecha_viaje y hora_salida son requeridos'
        }, status=400)
    
    try:
        fecha_obj = datetime.strptime(fecha_viaje, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({
            'success': False,
            'error': 'Formato de fecha inválido. Use YYYY-MM-DD'
        }, status=400)
    
    asientos_existentes = AsientoViaje.objects.filter(
        fecha_viaje=fecha_obj,
        hora_salida=hora_salida,
        origen=origen,
        destino=destino
    ).exists()
    
    if not asientos_existentes:
        AsientoViaje.inicializar_asientos_viaje(
            fecha_obj, hora_salida, origen, destino
        )
    
    asientos = AsientoViaje.objects.filter(
        fecha_viaje=fecha_obj,
        hora_salida=hora_salida,
        origen=origen,
        destino=destino
    ).order_by('piso', 'numero_asiento')
    
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
    
    total_asientos = asientos.count()
    total_disponibles = asientos.filter(ocupado=False).count()
    total_ocupados = asientos.filter(ocupado=True).count()
    
    return JsonResponse({
        'success': True,
        'piso1': asientos_piso1,
        'piso2': asientos_piso2,
        'total_asientos': total_asientos,
        'total_disponibles': total_disponibles,
        'total_ocupados': total_ocupados
    })


@csrf_exempt
@require_http_methods(["POST"])
def reservar_asiento_api(request):
    """API para reservar temporalmente un asiento"""
    try:
        data = json.loads(request.body)
        asiento_id = data.get('asiento_id')
        
        if not asiento_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del asiento es requerido'
            }, status=400)
        
        asiento = get_object_or_404(AsientoViaje, pk=asiento_id)
        
        if asiento.ocupado:
            return JsonResponse({
                'success': False,
                'error': 'El asiento ya está ocupado por otro pasajero'
            }, status=409)
        
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
@require_http_methods(["POST"])
def liberar_asiento_api(request):
    """API para liberar un asiento previamente reservado"""
    try:
        data = json.loads(request.body)
        asiento_id = data.get('asiento_id')
        
        if not asiento_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del asiento es requerido'
            }, status=400)
        
        asiento = get_object_or_404(AsientoViaje, pk=asiento_id)
        
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


@csrf_exempt
@require_http_methods(["GET"])
def verificar_asiento_api(request):
    """API para verificar si un asiento específico está disponible"""
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
    
    disponible = AsientoViaje.verificar_disponibilidad(
        fecha_obj, hora_salida, origen, destino, numero_asiento
    )
    
    return JsonResponse({
        'success': True,
        'disponible': disponible,
        'numero_asiento': numero_asiento
    })


@csrf_exempt
@require_http_methods(["POST"])
def crear_pasaje_api(request):
    """API para crear un pasaje desde React"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        data = json.loads(request.body)
        vendedor = User.objects.first()
        
        if not vendedor:
            return JsonResponse({
                'success': False,
                'error': 'No hay usuarios disponibles en el sistema'
            }, status=400)
        
        pasaje = Pasaje.objects.create(
            pasajero_id=data.get('pasajero'),
            fecha_viaje=data.get('fecha_viaje'),
            hora_salida=data.get('hora_salida'),
            origen=data.get('origen'),
            destino=data.get('destino'),
            numero_asiento=data.get('numero_asiento'),
            tipo_servicio=data.get('tipo_servicio'),
            precio=data.get('precio'),
            estado=data.get('estado', 'vendido'),
            vendedor=vendedor
        )
        
        return JsonResponse({
            'success': True,
            'id': pasaje.pk,
            'codigo_pasaje': pasaje.codigo_ticket if hasattr(pasaje, 'codigo_ticket') else str(pasaje.pk),
            'pasajero': pasaje.pasajero.id,
            'fecha_viaje': str(pasaje.fecha_viaje),
            'hora_salida': pasaje.hora_salida,
            'origen': pasaje.origen,
            'destino': pasaje.destino,
            'numero_asiento': pasaje.numero_asiento,
            'tipo_servicio': pasaje.tipo_servicio,
            'precio': str(pasaje.precio),
            'estado': pasaje.estado
        }, status=201)
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=400)


# ========================================
# APIs DE ADMINISTRACIÓN
# ========================================

@csrf_exempt
@require_http_methods(["GET"])
def listar_pasajeros_api(request):
    """API para listar todos los pasajeros registrados"""
    from pasajeros.models import Pasajero
    
    try:
        busqueda = request.GET.get('busqueda', '')
        pasajeros = Pasajero.objects.all().order_by('-fecha_registro')
        
        if busqueda:
            pasajeros = pasajeros.filter(
                Q(dni__icontains=busqueda) |
                Q(nombres__icontains=busqueda) |
                Q(apellidos__icontains=busqueda)
            )
        
        pasajeros_data = []
        for p in pasajeros:
            pasajeros_data.append({
                'id': p.pk,
                'dni': p.dni,
                'nombres': p.nombres,
                'apellidos': p.apellidos,
                'correo': p.correo,
                'telefono': p.telefono,
                'fecha_registro': str(p.fecha_registro),
                'total_viajes': p.pasajes.count()
            })
        
        return JsonResponse({
            'success': True,
            'pasajeros': pasajeros_data,
            'total': len(pasajeros_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def buscar_pasajero_por_dni_api(request):
    """API para buscar pasajero y sus pasajes por DNI"""
    from pasajeros.models import Pasajero
    
    try:
        dni = request.GET.get('dni', '')
        
        if not dni:
            return JsonResponse({
                'success': False,
                'error': 'El DNI es requerido'
            }, status=400)
        
        pasajeros = Pasajero.objects.filter(dni=dni)
        
        if not pasajeros.exists():
            return JsonResponse({
                'success': False,
                'error': 'No se encontró ningún pasajero con ese DNI'
            }, status=404)
        
        pasajero = pasajeros.order_by('-fecha_registro').first()
        pasajes = Pasaje.objects.filter(pasajero=pasajero).order_by('-fecha_venta')
        
        pasajes_data = []
        for p in pasajes:
            pasajes_data.append({
                'id': p.pk,
                'codigo_ticket': p.codigo_ticket,
                'fecha_viaje': str(p.fecha_viaje),
                'hora_salida': p.hora_salida,
                'origen': p.origen,
                'destino': p.destino,
                'numero_asiento': p.numero_asiento,
                'tipo_servicio': p.tipo_servicio,
                'precio': str(p.precio),
                'estado': p.estado,
                'fecha_venta': str(p.fecha_venta)
            })
        
        warning = None
        if pasajeros.count() > 1:
            warning = f'Se encontraron {pasajeros.count()} registros con este DNI. Mostrando el más reciente.'
        
        return JsonResponse({
            'success': True,
            'pasajero': {
                'id': pasajero.pk,
                'dni': pasajero.dni,
                'nombres': pasajero.nombres,
                'apellidos': pasajero.apellidos,
                'correo': pasajero.correo,
                'telefono': pasajero.telefono
            },
            'pasajes': pasajes_data,
            'total_pasajes': len(pasajes_data),
            'warning': warning
        })
        
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def listar_pasajes_api(request):
    """API para listar todos los pasajes vendidos"""
    try:
        estado = request.GET.get('estado', '')
        fecha_desde = request.GET.get('fecha_desde', '')
        fecha_hasta = request.GET.get('fecha_hasta', '')
        
        pasajes = Pasaje.objects.all().order_by('-fecha_venta')
        
        if estado:
            pasajes = pasajes.filter(estado=estado)
        
        if fecha_desde:
            fecha_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
            pasajes = pasajes.filter(fecha_venta__gte=fecha_obj)
        
        if fecha_hasta:
            fecha_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
            pasajes = pasajes.filter(fecha_venta__lte=fecha_obj)
        
        pasajes_data = []
        for p in pasajes:
            pasajes_data.append({
                'id': p.pk,
                'codigo_ticket': p.codigo_ticket,
                'pasajero': {
                    'dni': p.pasajero.dni,
                    'nombres': p.pasajero.nombres,
                    'apellidos': p.pasajero.apellidos
                },
                'fecha_viaje': str(p.fecha_viaje),
                'hora_salida': p.hora_salida,
                'origen': p.origen,
                'destino': p.destino,
                'numero_asiento': p.numero_asiento,
                'tipo_servicio': p.tipo_servicio,
                'precio': str(p.precio),
                'estado': p.estado,
                'fecha_venta': str(p.fecha_venta)
            })
        
        return JsonResponse({
            'success': True,
            'pasajes': pasajes_data,
            'total': len(pasajes_data)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def editar_pasaje_api(request):
    """API para editar un pasaje existente"""
    try:
        data = json.loads(request.body)
        pasaje_id = data.get('pasaje_id')
        
        if not pasaje_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del pasaje es requerido'
            }, status=400)
        
        pasaje = get_object_or_404(Pasaje, pk=pasaje_id)
        
        if 'fecha_viaje' in data:
            pasaje.fecha_viaje = data['fecha_viaje']
        if 'hora_salida' in data:
            pasaje.hora_salida = data['hora_salida']
        if 'tipo_servicio' in data:
            pasaje.tipo_servicio = data['tipo_servicio']
        if 'precio' in data:
            pasaje.precio = data['precio']
        
        pasaje.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Pasaje actualizado exitosamente',
            'pasaje_id': pasaje.pk
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def visualizar_asientos_api(request):
    """API para visualizar qué pasajero compró cada asiento"""
    try:
        fecha = request.GET.get('fecha')
        hora = request.GET.get('hora', '22:00')
        origen = request.GET.get('origen', 'Lima')
        destino = request.GET.get('destino', 'Ferreñafe')
        
        if not fecha:
            fecha = datetime.now().date()
        else:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        pasajes = Pasaje.objects.filter(
            fecha_viaje=fecha,
            hora_salida=hora,
            origen=origen,
            destino=destino
        ).exclude(estado='anulado')
        
        asientos_ocupados = []
        for p in pasajes:
            asientos_ocupados.append({
                'numero_asiento': p.numero_asiento,
                'pasajero': {
                    'dni': p.pasajero.dni,
                    'nombres': p.pasajero.nombres,
                    'apellidos': p.pasajero.apellidos,
                    'telefono': p.pasajero.telefono
                },
                'codigo_ticket': p.codigo_ticket,
                'precio': str(p.precio),
                'estado': p.estado,
                'pasaje_id': p.pk
            })
        
        return JsonResponse({
            'success': True,
            'fecha': str(fecha),
            'hora': hora,
            'ruta': f"{origen} → {destino}",
            'asientos_ocupados': asientos_ocupados,
            'total_ocupados': len(asientos_ocupados)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def reporte_diario_api(request):
    """API para generar reporte de ventas diarias"""
    try:
        fecha = request.GET.get('fecha')
        
        if not fecha:
            fecha = datetime.now().date()
        else:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        pasajes = Pasaje.objects.filter(
            fecha_venta__date=fecha
        ).exclude(estado='anulado')
        
        total_vendidos = pasajes.count()
        total_recaudado = pasajes.aggregate(Sum('precio'))['precio__sum'] or 0
        
        por_estado = {}
        for estado in ['vendido', 'reservado', 'anulado']:
            por_estado[estado] = Pasaje.objects.filter(
                fecha_venta__date=fecha,
                estado=estado
            ).count()
        
        por_ruta = []
        rutas = pasajes.values('origen', 'destino').annotate(
            cantidad=Count('id'),
            total=Sum('precio')
        )
        
        for ruta in rutas:
            por_ruta.append({
                'ruta': f"{ruta['origen']} → {ruta['destino']}",
                'cantidad': ruta['cantidad'],
                'total': str(ruta['total'])
            })
        
        return JsonResponse({
            'success': True,
            'fecha': str(fecha),
            'resumen': {
                'total_vendidos': total_vendidos,
                'total_recaudado': str(total_recaudado),
                'por_estado': por_estado
            },
            'por_ruta': por_ruta
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def reporte_mensual_api(request):
    """API para generar reporte de ventas mensuales"""
    try:
        mes = request.GET.get('mes')
        
        if not mes:
            hoy = datetime.now()
            anio = hoy.year
            mes_num = hoy.month
        else:
            anio, mes_num = mes.split('-')
            anio = int(anio)
            mes_num = int(mes_num)
        
        pasajes = Pasaje.objects.filter(
            fecha_venta__year=anio,
            fecha_venta__month=mes_num
        ).exclude(estado='anulado')
        
        total_vendidos = pasajes.count()
        total_recaudado = pasajes.aggregate(Sum('precio'))['precio__sum'] or 0
        
        por_dia = []
        dias_con_ventas = pasajes.values('fecha_venta__date').annotate(
            cantidad=Count('id'),
            total=Sum('precio')
        ).order_by('fecha_venta__date')
        
        for dia in dias_con_ventas:
            por_dia.append({
                'fecha': str(dia['fecha_venta__date']),
                'cantidad': dia['cantidad'],
                'total': str(dia['total'])
            })
        
        return JsonResponse({
            'success': True,
            'periodo': f"{anio}-{mes_num:02d}",
            'resumen': {
                'total_vendidos': total_vendidos,
                'total_recaudado': str(total_recaudado)
            },
            'por_dia': por_dia
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def reporte_anual_api(request):
    """API para generar reporte de ventas anuales"""
    try:
        anio = request.GET.get('anio')
        
        if not anio:
            anio = datetime.now().year
        else:
            anio = int(anio)
        
        pasajes = Pasaje.objects.filter(
            fecha_venta__year=anio
        ).exclude(estado='anulado')
        
        total_vendidos = pasajes.count()
        total_recaudado = pasajes.aggregate(Sum('precio'))['precio__sum'] or 0
        
        por_mes = []
        meses_con_ventas = pasajes.values('fecha_venta__month').annotate(
            cantidad=Count('id'),
            total=Sum('precio')
        ).order_by('fecha_venta__month')
        
        meses_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        for mes in meses_con_ventas:
            por_mes.append({
                'mes': meses_nombres[mes['fecha_venta__month'] - 1],
                'mes_numero': mes['fecha_venta__month'],
                'cantidad': mes['cantidad'],
                'total': str(mes['total'])
            })
        
        return JsonResponse({
            'success': True,
            'anio': anio,
            'resumen': {
                'total_vendidos': total_vendidos,
                'total_recaudado': str(total_recaudado)
            },
            'por_mes': por_mes
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# ========================================
# APIs DE EDICIÓN Y ELIMINACIÓN
# ========================================

@csrf_exempt
@require_http_methods(["POST"])
def editar_pasajero_api(request):
    """API para editar un pasajero existente"""
    from pasajeros.models import Pasajero
    
    try:
        data = json.loads(request.body)
        pasajero_id = data.get('pasajero_id')
        
        if not pasajero_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del pasajero es requerido'
            }, status=400)
        
        pasajero = get_object_or_404(Pasajero, pk=pasajero_id)
        
        if 'nombres' in data:
            pasajero.nombres = data['nombres']
        if 'apellidos' in data:
            pasajero.apellidos = data['apellidos']
        if 'correo' in data:
            pasajero.correo = data['correo']
        if 'telefono' in data:
            pasajero.telefono = data['telefono']
        
        pasajero.save()
        
        return JsonResponse({
            'success': True,
            'mensaje': 'Pasajero actualizado exitosamente',
            'pasajero': {
                'id': pasajero.pk,
                'dni': pasajero.dni,
                'nombres': pasajero.nombres,
                'apellidos': pasajero.apellidos,
                'correo': pasajero.correo,
                'telefono': pasajero.telefono
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def eliminar_pasajero_api(request):
    """API para eliminar un pasajero"""
    from pasajeros.models import Pasajero
    
    try:
        data = json.loads(request.body)
        pasajero_id = data.get('pasajero_id')
        
        if not pasajero_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del pasajero es requerido'
            }, status=400)
        
        pasajero = get_object_or_404(Pasajero, pk=pasajero_id)
        
        if pasajero.pasajes.exists():
            return JsonResponse({
                'success': False,
                'error': f'No se puede eliminar el pasajero porque tiene {pasajero.pasajes.count()} pasajes asociados'
            }, status=400)
        
        nombre_completo = f"{pasajero.nombres} {pasajero.apellidos}"
        pasajero.delete()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Pasajero {nombre_completo} eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def eliminar_pasaje_api(request):
    """API para eliminar un pasaje"""
    try:
        data = json.loads(request.body)
        pasaje_id = data.get('pasaje_id')
        
        if not pasaje_id:
            return JsonResponse({
                'success': False,
                'error': 'El ID del pasaje es requerido'
            }, status=400)
        
        pasaje = get_object_or_404(Pasaje, pk=pasaje_id)
        
        try:
            asiento = AsientoViaje.objects.get(
                fecha_viaje=pasaje.fecha_viaje,
                hora_salida=pasaje.hora_salida,
                origen=pasaje.origen,
                destino=pasaje.destino,
                numero_asiento=pasaje.numero_asiento
            )
            asiento.ocupado = False
            asiento.save()
        except AsientoViaje.DoesNotExist:
            pass
        
        codigo = pasaje.codigo_ticket
        pasaje.delete()
        
        return JsonResponse({
            'success': True,
            'mensaje': f'Pasaje {codigo} eliminado exitosamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)