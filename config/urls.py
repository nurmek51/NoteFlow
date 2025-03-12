from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),  # Подключаем users.urls
    path('api/', include('apps.materials.urls')) # Включил материалы корочежиесть
]
