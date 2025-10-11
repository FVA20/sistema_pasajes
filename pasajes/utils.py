from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from datetime import datetime


def generar_ticket_pdf(pasaje):
    """Genera un PDF del ticket de pasaje"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width/2, height - 80, "VÍA PACÍFICO")
    
    # Subtítulo
    p.setFont("Helvetica", 14)
    p.drawCentredString(width/2, height - 110, "Ticket de Pasaje")
    
    # Línea divisoria
    p.line(50, height - 130, width - 50, height - 130)
    
    # Información del ticket
    y = height - 170
    p.setFont("Helvetica-Bold", 12)
    
    # Código de ticket
    p.drawString(80, y, "CÓDIGO DE TICKET:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.codigo_ticket)
    
    # Pasajero
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "PASAJERO:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.pasajero.nombre_completo)
    
    # DNI
    y -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "DNI:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.pasajero.dni)
    
    # Origen - Destino
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "RUTA:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, f"{pasaje.origen} → {pasaje.destino}")
    
    # Fecha de viaje
    y -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "FECHA:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.fecha_viaje.strftime('%d/%m/%Y'))
    
    # Hora de salida
    y -= 25
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "HORA:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.hora_salida.strftime('%H:%M'))
    
    # Asiento
    y -= 30
    p.setFont("Helvetica-Bold", 14)
    p.drawString(80, y, "ASIENTO:")
    p.setFont("Helvetica-Bold", 18)
    p.drawString(250, y, str(pasaje.numero_asiento))
    
    # Tipo de servicio
    y -= 30
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "SERVICIO:")
    p.setFont("Helvetica", 12)
    p.drawString(250, y, pasaje.get_tipo_servicio_display())
    
    # Equipaje
    if pasaje.lleva_equipaje:
        y -= 25
        p.setFont("Helvetica", 11)
        p.drawString(80, y, f"Equipaje: {pasaje.cantidad_maletas} maleta(s)")
    
    if pasaje.lleva_encomienda:
        y -= 20
        p.setFont("Helvetica", 11)
        p.drawString(80, y, f"Encomienda: {pasaje.peso_encomienda} kg")
    
    # Precio
    y -= 40
    p.line(50, y, width - 50, y)
    y -= 30
    p.setFont("Helvetica-Bold", 14)
    p.drawString(80, y, "TOTAL:")
    p.setFont("Helvetica-Bold", 16)
    p.drawString(250, y, f"S/ {pasaje.total_pagar}")
    
    # Fecha de emisión
    y -= 60
    p.setFont("Helvetica", 9)
    p.drawString(80, y, f"Fecha de emisión: {pasaje.fecha_venta.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(80, y - 15, f"Vendedor: {pasaje.vendedor.username}")
    
    # Términos
    y -= 50
    p.setFont("Helvetica", 8)
    p.drawString(80, y, "Términos: Presentarse 15 minutos antes de la salida.")
    p.drawString(80, y - 12, "El pasaje no es reembolsable 12 horas antes de la salida.")
    
    # Pie de página
    p.setFont("Helvetica-Oblique", 9)
    p.drawCentredString(width/2, 50, "Gracias por viajar con VÍA PACÍFICO")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer