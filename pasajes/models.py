from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import uuid


class Pasaje(models.Model):
    """
    Modelo principal para la venta de pasajes
    """
    
    ESTADO_CHOICES = [
        ('vigente', 'Vigente'),
        ('usado', 'Usado'),
        ('anulado', 'Anulado'),
    ]
    
    TIPO_SERVICIO_CHOICES = [
        ('economico', 'Económico'),
        ('vip', 'VIP'),
        ('cama', 'Semi Cama'),
        ('suite', 'Suite'),
    ]
    
    # Identificación única
    codigo_ticket = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name='Código de Ticket',
        db_index=True
    )
    
    # Relación con pasajero
    pasajero = models.ForeignKey(
        'pasajeros.Pasajero',
        on_delete=models.PROTECT,
        related_name='pasajes',
        verbose_name='Pasajero'
    )
    
    # Datos del viaje
    fecha_viaje = models.DateField(
        verbose_name='Fecha de Viaje',
        db_index=True
    )
    
    hora_salida = models.TimeField(
        verbose_name='Hora de Salida'
    )
    
    origen = models.CharField(
        max_length=100,
        default='Lima',
        verbose_name='Origen'
    )
    
    destino = models.CharField(
        max_length=100,
        default='Ferreñafe',
        verbose_name='Destino'
    )
    
    # Asiento
    numero_asiento = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Número de Asiento'
    )
    
    # Tipo de servicio y precio
    tipo_servicio = models.CharField(
        max_length=20,
        choices=TIPO_SERVICIO_CHOICES,
        default='economico',
        verbose_name='Tipo de Servicio'
    )
    
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio del Pasaje'
    )
    
    # Equipaje y encomiendas
    lleva_equipaje = models.BooleanField(
        default=False,
        verbose_name='Lleva Equipaje'
    )
    
    cantidad_maletas = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad de Maletas'
    )
    
    lleva_encomienda = models.BooleanField(
        default=False,
        verbose_name='Lleva Encomienda'
    )
    
    descripcion_encomienda = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción de Encomienda'
    )
    
    peso_encomienda = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Peso de Encomienda (kg)'
    )
    
    cargo_adicional = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(0)],
        verbose_name='Cargo Adicional'
    )
    
    # Estado del pasaje
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='vigente',
        verbose_name='Estado',
        db_index=True
    )
    
    # Auditoría de venta
    vendedor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='pasajes_vendidos',
        verbose_name='Vendedor'
    )
    
    fecha_venta = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Venta'
    )
    
    # Anulación
    fecha_anulacion = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Fecha de Anulación'
    )
    
    motivo_anulacion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Motivo de Anulación'
    )
    
    anulado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pasajes_anulados',
        verbose_name='Anulado Por'
    )
    
    monto_reembolso = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name='Monto de Reembolso'
    )
    
    # Contador de ediciones
    numero_ediciones = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de Ediciones'
    )
    
    # Timestamps
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    class Meta:
        db_table = 'pasajes'
        verbose_name = 'Pasaje'
        verbose_name_plural = 'Pasajes'
        ordering = ['-fecha_venta']
        unique_together = [['fecha_viaje', 'hora_salida', 'numero_asiento']]
        indexes = [
            models.Index(fields=['codigo_ticket']),
            models.Index(fields=['fecha_viaje', 'estado']),
            models.Index(fields=['pasajero', 'estado']),
            models.Index(fields=['-fecha_venta']),
        ]
    
    def __str__(self):
        return f"Ticket {self.codigo_ticket} - Asiento {self.numero_asiento}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_ticket:
            self.codigo_ticket = self.generar_codigo_ticket()
        super().save(*args, **kwargs)
    
    def generar_codigo_ticket(self):
        fecha = datetime.now().strftime('%Y%m%d')
        uuid_corto = str(uuid.uuid4())[:8].upper()
        return f"TKT-{fecha}-{uuid_corto}"
    
    @property
    def total_pagar(self):
        return self.precio + self.cargo_adicional
    
    @property
    def puede_editarse(self):
        if self.estado != 'vigente':
            return False
        fecha_hora_viaje = datetime.combine(self.fecha_viaje, self.hora_salida)
        fecha_hora_viaje = timezone.make_aware(fecha_hora_viaje)
        tiempo_limite = fecha_hora_viaje - timedelta(hours=1)
        return timezone.now() < tiempo_limite
    
    @property
    def puede_anularse(self):
        if self.estado in ['anulado', 'usado']:
            return False
        fecha_hora_viaje = datetime.combine(self.fecha_viaje, self.hora_salida)
        fecha_hora_viaje = timezone.make_aware(fecha_hora_viaje)
        tiempo_limite = fecha_hora_viaje - timedelta(hours=1)
        return timezone.now() < tiempo_limite
    
    def calcular_reembolso(self):
        from django.conf import settings
        fecha_hora_viaje = datetime.combine(self.fecha_viaje, self.hora_salida)
        fecha_hora_viaje = timezone.make_aware(fecha_hora_viaje)
        horas_restantes = (fecha_hora_viaje - timezone.now()).total_seconds() / 3600
        
        config = settings.PASAJES_CONFIG
        if horas_restantes >= 24:
            porcentaje = config['REEMBOLSO_24H']
        elif horas_restantes >= 12:
            porcentaje = config['REEMBOLSO_12H']
        else:
            porcentaje = config['REEMBOLSO_MENOS_12H']
        
        return float(self.total_pagar) * porcentaje
    
    def anular(self, usuario, motivo):
        if not self.puede_anularse:
            raise ValidationError("Este pasaje no puede ser anulado")
        
        self.estado = 'anulado'
        self.fecha_anulacion = timezone.now()
        self.motivo_anulacion = motivo
        self.anulado_por = usuario
        self.monto_reembolso = self.calcular_reembolso()
        self.save()