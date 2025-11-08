import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pasajes.models import AsientoViaje
from datetime import date, time

AsientoViaje.objects.all().delete()

for num in range(1, 11):p
    AsientoViaje.objects.create(
        fecha_viaje=date(2025, 11, 7),
        hora_salida=time(11, 14, 0),
        origen='Lima',
        destino='Ferreñafe',
        numero_asiento=num,
        piso=1,
        ocupado=False
    )

for num in range(1, 21):
    AsientoViaje.objects.create(
        fecha_viaje=date(2025, 11, 7),
        hora_salida=time(11, 14, 0),
        origen='Lima',
        destino='Ferreñafe',
        numero_asiento=num,
        piso=2,
        ocupado=False
    )

print(f"✅ Piso 1: {AsientoViaje.objects.filter(piso=1).count()}")
print(f"✅ Piso 2: {AsientoViaje.objects.filter(piso=2).count()}")