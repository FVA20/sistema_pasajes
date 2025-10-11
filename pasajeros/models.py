from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date


class Pasajero(models.Model):
    """
    Modelo para almacenar información de pasajeros
    """
    
    # Validadores
    dni_validator = RegexValidator(
        regex=r'^\d{8}$',
        message='El DNI debe tener exactamente 8 dígitos'
    )
    
    telefono_validator = RegexValidator(
        regex=r'^9\d{8}$',
        message='El teléfono debe tener 9 dígitos y comenzar con 9'
    )
    
    # Campos principales
    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres',
        help_text='Nombres completos del pasajero'
    )
    
    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos',
        help_text='Apellidos completos del pasajero'
    )
    
    dni = models.CharField(
        max_length=8,
        validators=[dni_validator],
        unique=False,
        verbose_name='DNI',
        help_text='Documento Nacional de Identidad',
        db_index=True
    )
    
    fecha_nacimiento = models.DateField(
        verbose_name='Fecha de Nacimiento',
        help_text='Fecha de nacimiento del pasajero'
    )
    
    telefono = models.CharField(
        max_length=9,
        validators=[telefono_validator],
        verbose_name='Teléfono Celular'
    )
    
    correo = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        verbose_name='Correo Electrónico',
        help_text='Correo electrónico (opcional)'
    )
    
    # Campos de auditoría
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        db_table = 'pasajeros'
        verbose_name = 'Pasajero'
        verbose_name_plural = 'Pasajeros'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['dni', 'apellidos']),
            models.Index(fields=['telefono']),
        ]
    
    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - {self.dni}"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del pasajero"""
        return f"{self.nombres} {self.apellidos}"
    
    @property
    def edad(self):
        """Calcula la edad del pasajero"""
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < 
            (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )
    
    @property
    def es_menor_edad(self):
        """Verifica si el pasajero es menor de edad"""
        return self.edad < 18
    
    def clean(self):
        """Validaciones personalizadas"""
        super().clean()
        
        if self.fecha_nacimiento > date.today():
            raise ValidationError({
                'fecha_nacimiento': 'La fecha de nacimiento no puede ser futura'
            })
        
        if self.edad < 1:
            raise ValidationError({
                'fecha_nacimiento': 'El pasajero debe tener al menos 1 año'
            })
        
        if self.edad > 120:
            raise ValidationError({
                'fecha_nacimiento': 'La fecha de nacimiento no es válida'
            })
    
    def save(self, *args, **kwargs):
        """Override del método save para validaciones"""
        self.nombres = self.nombres.strip().title()
        self.apellidos = self.apellidos.strip().title()
        
        if self.correo:
            self.correo = self.correo.strip().lower()
        
        self.full_clean()
        super().save(*args, **kwargs)