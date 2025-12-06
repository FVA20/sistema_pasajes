from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pasajeros/', include('pasajeros.urls')),  # ← DEBE ESTAR
    path('pasajes/', include('pasajes.urls')),      # ← DEBE ESTAR
    path('reportes/', include('reportes.urls')),
]