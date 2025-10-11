from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from pasajes.models import Pasaje
from reportes.models import ReporteVenta
import json


@login_required
def reporte_diario(request):
    """Genera reporte de ventas del día"""
    fecha = request.GET.get('fecha', timezone.now().date())
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
    
    pasajes = Pasaje.objects.filter(fecha_venta__date=fecha)
    
    total_pasajes = pasajes.count()
    pasajes_vigentes = pasajes.filter(estado='vigente').count()
    pasajes_anulados = pasajes.filter(estado='anulado').count()
    
    total_ingresos = pasajes.filter(estado__in=['vigente', 'usado']).aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    ingresos_perdidos = pasajes.filter(estado='anulado').aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    con_equipaje = pasajes.filter(lleva_equipaje=True).count()
    con_encomienda = pasajes.filter(lleva_encomienda=True).count()
    
    pasajes_por_hora = pasajes.values('hora_salida').annotate(
        total=Count('id')
    ).order_by('hora_salida')
    
    context = {
        'fecha': fecha,
        'total_pasajes': total_pasajes,
        'pasajes_vigentes': pasajes_vigentes,
        'pasajes_anulados': pasajes_anulados,
        'total_ingresos': total_ingresos,
        'ingresos_perdidos': ingresos_perdidos,
        'con_equipaje': con_equipaje,
        'con_encomienda': con_encomienda,
        'pasajes_por_hora': pasajes_por_hora,
        'pasajes': pasajes[:20]
    }
    
    return render(request, 'reportes/diario.html', context)


@login_required
def reporte_mensual(request):
    """Genera reporte de ventas del mes"""
    mes = request.GET.get('mes', timezone.now().month)
    anio = request.GET.get('anio', timezone.now().year)
    
    mes = int(mes)
    anio = int(anio)
    
    fecha_inicio = datetime(anio, mes, 1).date()
    if mes == 12:
        fecha_fin = datetime(anio + 1, 1, 1).date() - timedelta(days=1)
    else:
        fecha_fin = datetime(anio, mes + 1, 1).date() - timedelta(days=1)
    
    pasajes = Pasaje.objects.filter(
        fecha_venta__date__gte=fecha_inicio,
        fecha_venta__date__lte=fecha_fin
    )
    
    total_pasajes = pasajes.count()
    pasajes_vigentes = pasajes.filter(estado='vigente').count()
    pasajes_anulados = pasajes.filter(estado='anulado').count()
    
    total_ingresos = pasajes.filter(estado__in=['vigente', 'usado']).aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    dias_transcurridos = (timezone.now().date() - fecha_inicio).days + 1
    promedio_diario = total_pasajes / dias_transcurridos if dias_transcurridos > 0 else 0
    
    ventas_por_dia = pasajes.extra(
        select={'dia': 'DATE(fecha_venta)'}
    ).values('dia').annotate(
        total=Count('id'),
        ingresos=Sum('precio')
    ).order_by('dia')
    
    por_servicio = pasajes.values('tipo_servicio').annotate(
        total=Count('id')
    ).order_by('-total')
    
    por_vendedor = pasajes.values('vendedor__username').annotate(
        total=Count('id'),
        ingresos=Sum('precio')
    ).order_by('-total')
    
    context = {
        'mes': mes,
        'anio': anio,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_pasajes': total_pasajes,
        'pasajes_vigentes': pasajes_vigentes,
        'pasajes_anulados': pasajes_anulados,
        'total_ingresos': total_ingresos,
        'promedio_diario': round(promedio_diario, 2),
        'ventas_por_dia': list(ventas_por_dia),
        'por_servicio': por_servicio,
        'por_vendedor': por_vendedor,
    }
    
    return render(request, 'reportes/mensual.html', context)


@login_required
def reporte_anual(request):
    """Genera reporte de ventas del año"""
    anio = request.GET.get('anio', timezone.now().year)
    anio = int(anio)
    
    fecha_inicio = datetime(anio, 1, 1).date()
    fecha_fin = datetime(anio, 12, 31).date()
    
    pasajes = Pasaje.objects.filter(
        fecha_venta__date__gte=fecha_inicio,
        fecha_venta__date__lte=fecha_fin
    )
    
    total_pasajes = pasajes.count()
    pasajes_vigentes = pasajes.filter(estado='vigente').count()
    pasajes_anulados = pasajes.filter(estado='anulado').count()
    
    total_ingresos = pasajes.filter(estado__in=['vigente', 'usado']).aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    promedio_mensual = total_pasajes / 12
    
    ventas_por_mes = pasajes.extra(
        select={'mes': 'EXTRACT(MONTH FROM fecha_venta)'}
    ).values('mes').annotate(
        total=Count('id'),
        ingresos=Sum('precio')
    ).order_by('mes')
    
    if ventas_por_mes:
        mes_pico = max(ventas_por_mes, key=lambda x: x['total'])
        mes_valle = min(ventas_por_mes, key=lambda x: x['total'])
    else:
        mes_pico = None
        mes_valle = None
    
    primer_semestre = pasajes.filter(fecha_venta__month__lte=6).count()
    segundo_semestre = pasajes.filter(fecha_venta__month__gt=6).count()
    
    context = {
        'anio': anio,
        'total_pasajes': total_pasajes,
        'pasajes_vigentes': pasajes_vigentes,
        'pasajes_anulados': pasajes_anulados,
        'total_ingresos': total_ingresos,
        'promedio_mensual': round(promedio_mensual, 2),
        'ventas_por_mes': list(ventas_por_mes),
        'mes_pico': mes_pico,
        'mes_valle': mes_valle,
        'primer_semestre': primer_semestre,
        'segundo_semestre': segundo_semestre,
    }
    
    return render(request, 'reportes/anual.html', context)


@login_required
def dashboard(request):
    """Dashboard principal con resumen de reportes"""
    hoy = timezone.now().date()
    
    pasajes_hoy = Pasaje.objects.filter(fecha_venta__date=hoy)
    total_hoy = pasajes_hoy.count()
    ingresos_hoy = pasajes_hoy.filter(estado__in=['vigente', 'usado']).aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    mes_actual = hoy.month
    anio_actual = hoy.year
    pasajes_mes = Pasaje.objects.filter(
        fecha_venta__month=mes_actual,
        fecha_venta__year=anio_actual
    )
    total_mes = pasajes_mes.count()
    ingresos_mes = pasajes_mes.filter(estado__in=['vigente', 'usado']).aggregate(
        total=Sum('precio')
    )['total'] or 0
    
    fecha_limite = hoy + timedelta(days=7)
    pasajes_proximos = Pasaje.objects.filter(
        fecha_viaje__gte=hoy,
        fecha_viaje__lte=fecha_limite,
        estado='vigente'
    ).count()
    
    context = {
        'total_hoy': total_hoy,
        'ingresos_hoy': ingresos_hoy,
        'total_mes': total_mes,
        'ingresos_mes': ingresos_mes,
        'pasajes_proximos': pasajes_proximos,
    }
    
    return render(request, 'reportes/dashboard.html', context)