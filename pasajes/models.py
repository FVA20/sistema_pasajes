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
        
        # Marcar el asiento como ocupado al guardar
        if self.pk is None and self.estado == 'vigente':  # Nuevo pasaje
            AsientoViaje.objects.filter(
                fecha_viaje=self.fecha_viaje,
                hora_salida=self.hora_salida,
                origen=self.origen,
                destino=self.destino,
                numero_asiento=self.numero_asiento
            ).update(ocupado=True)
        
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
        
        # Liberar el asiento al anular
        AsientoViaje.objects.filter(
            fecha_viaje=self.fecha_viaje,
            hora_salida=self.hora_salida,
            origen=self.origen,
            destino=self.destino,
            numero_asiento=self.numero_asiento,
            pasaje=self
        ).update(ocupado=False, pasaje=None)
        
        self.save()


# ========================================
# NUEVOS MODELOS PARA SELECCIÓN DE ASIENTOS
# ========================================

class ConfiguracionBus(models.Model):
    """
    Configuración de la distribución de asientos del bus
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Bus')
    tipo_servicio = models.CharField(
        max_length=20,
        choices=[
            ('economico', 'Económico'),
            ('vip', 'VIP'),
            ('cama', 'Semi Cama'),
            ('suite', 'Suite'),
        ],
        verbose_name='Tipo de Servicio'
    )
    pisos = models.IntegerField(default=2, verbose_name='Número de Pisos')
    total_asientos = models.IntegerField(default=60, verbose_name='Total de Asientos')
    asientos_piso1 = models.IntegerField(default=12, verbose_name='Asientos Piso 1')
    asientos_piso2 = models.IntegerField(default=48, verbose_name='Asientos Piso 2')
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'configuracion_buses'
        verbose_name = 'Configuración de Bus'
        verbose_name_plural = 'Configuraciones de Buses'
    
    def __str__(self):
        # NO usar get_tipo_servicio_display, hacer el mapeo manual
        tipos = {
            'economico': 'Económico',
            'vip': 'VIP',
            'cama': 'Semi Cama',
            'suite': 'Suite',
        }
        tipo_display = tipos.get(self.tipo_servicio, self.tipo_servicio)
        return f"{self.nombre} - {tipo_display}"


class AsientoViaje(models.Model):
    """
    Control de asientos disponibles/ocupados por viaje
    Sistema en tiempo real para evitar ventas duplicadas
    """
    fecha_viaje = models.DateField(verbose_name='Fecha de Viaje', db_index=True)
    hora_salida = models.TimeField(verbose_name='Hora de Salida')
    origen = models.CharField(max_length=100, default='Lima')
    destino = models.CharField(max_length=100, default='Ferreñafe')
    numero_asiento = models.IntegerField(verbose_name='Número de Asiento')
    piso = models.IntegerField(default=1, verbose_name='Piso')
    ocupado = models.BooleanField(default=False, db_index=True)
    
    # Relación con el pasaje (se establece al confirmar la venta)
    pasaje = models.OneToOneField(
        'Pasaje',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asiento_reservado'
    )
    
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'asientos_viaje'
        unique_together = [['fecha_viaje', 'hora_salida', 'origen', 'destino', 'piso', 'numero_asiento']]
        verbose_name = 'Asiento de Viaje'
        verbose_name_plural = 'Asientos de Viaje'
        ordering = ['fecha_viaje', 'piso', 'numero_asiento']
        indexes = [
            models.Index(fields=['fecha_viaje', 'hora_salida', 'ocupado']),
            models.Index(fields=['fecha_viaje', 'hora_salida', 'origen', 'destino']),
        ]
    
    def __str__(self):
        estado = "Ocupado" if self.ocupado else "Disponible"
        return f"Asiento {self.numero_asiento} Piso {self.piso} - {estado}"
    
    @classmethod
    def inicializar_asientos_viaje(cls, fecha_viaje, hora_salida, origen, destino, configuracion=None):
        """
        Crear todos los asientos para un viaje específico
        Si ya existen, no hace nada
        Piso 1: 10 asientos (1-10)
        Piso 2: 20 asientos (1-20)
        """
        # Verificar si ya existen asientos para este viaje
        asientos_existentes = cls.objects.filter(
            fecha_viaje=fecha_viaje,
            hora_salida=hora_salida,
            origen=origen,
            destino=destino
        ).exists()
        
        if asientos_existentes:
            return False  # Ya existen asientos
        
        # Crear asientos para piso 1 (10 asientos: del 1 al 10)
        for num in range(1, 11):
            cls.objects.create(
                fecha_viaje=fecha_viaje,
                hora_salida=hora_salida,
                origen=origen,
                destino=destino,
                numero_asiento=num,
                piso=1,
                ocupado=False
            )
        
        # Crear asientos para piso 2 (20 asientos: del 1 al 20)
        for num in range(1, 21):
            cls.objects.create(
                fecha_viaje=fecha_viaje,
                hora_salida=hora_salida,
                origen=origen,
                destino=destino,
                numero_asiento=num,
                piso=2,
                ocupado=False
            )
        
        return True
    
    @classmethod
    def obtener_asientos_disponibles(cls, fecha_viaje, hora_salida, origen, destino):
        """
        Obtener todos los asientos con su estado de disponibilidad
        """
        # Inicializar asientos si no existen
        cls.inicializar_asientos_viaje(fecha_viaje, hora_salida, origen, destino)
        
        # Retornar todos los asientos ordenados
        return cls.objects.filter(
            fecha_viaje=fecha_viaje,
            hora_salida=hora_salida,
            origen=origen,
            destino=destino
        ).order_by('piso', 'numero_asiento')
    
    @classmethod
    def verificar_disponibilidad(cls, fecha_viaje, hora_salida, origen, destino, numero_asiento):
        """
        Verificar si un asiento específico está disponible
        """
        try:
            asiento = cls.objects.get(
                fecha_viaje=fecha_viaje,
                hora_salida=hora_salida,
                origen=origen,
                destino=destino,
                numero_asiento=numero_asiento
            )
            return not asiento.ocupado
        except cls.DoesNotExist:
            return False
    
    def reservar(self):
        """
        Marcar asiento como ocupado
        """
        if self.ocupado:
            raise ValidationError("Este asiento ya está ocupado")
        self.ocupado = True
        self.save()
    
    def liberar(self):
        """
        Marcar asiento como disponible
        """
        self.ocupado = False
        self.pasaje = None
        self.save()