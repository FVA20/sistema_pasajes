from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal


class ReporteVenta(models.Model):
    """
    Modelo para almacenar reportes generados
    """
    TIPO_CHOICES = [
        ('diario', 'Diario'),
        ('mensual', 'Mensual'),
        ('anual', 'Anual'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_ingresos = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    pasajes_anulados = models.IntegerField(default=0)
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reportes_venta'
        verbose_name = 'Reporte de Venta'
        verbose_name_plural = 'Reportes de Venta'
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"Reporte {self.tipo} - {self.fecha_inicio} a {self.fecha_fin}"