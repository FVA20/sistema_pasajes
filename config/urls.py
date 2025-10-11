from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/reportes/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('reportes/', include('reportes.urls')),
    path('pasajes/', include('pasajes.urls')),
]