from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('auth.urls')),
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
]
