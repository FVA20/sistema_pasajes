from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Pasajero
from datetime import date
import json


@csrf_exempt
@require_http_methods(["POST"])
def crear_pasajero_api(request):
    """API para crear un pasajero desde React"""
    try:
        data = json.loads(request.body)
        
        # Crear el pasajero con los campos correctos del modelo
        pasajero = Pasajero.objects.create(
            dni=data.get('numero_documento'),
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            correo=data.get('email'),
            telefono=data.get('telefono'),
            fecha_nacimiento=date(2000, 1, 1)  # Fecha por defecto ya que es obligatoria
        )
        
        return JsonResponse({
            'success': True,
            'id': pasajero.pk,
            'tipo_documento': 'DNI',
            'numero_documento': pasajero.dni,
            'nombres': pasajero.nombres,
            'apellidos': pasajero.apellidos,
            'email': pasajero.correo,
            'telefono': pasajero.telefono
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)