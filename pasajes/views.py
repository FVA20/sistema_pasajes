from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pasaje
from .utils import generar_ticket_pdf


@login_required
def descargar_ticket(request, pasaje_id):
    """Descarga el ticket en PDF"""
    pasaje = get_object_or_404(Pasaje, id=pasaje_id)
    
    pdf = generar_ticket_pdf(pasaje)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{pasaje.codigo_ticket}.pdf"'
    
    return response