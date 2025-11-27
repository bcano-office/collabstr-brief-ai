"""
URL configuration for collabstr_ai project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from brief_generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/generate-brief/', views.generate_brief, name='generate_brief'),
    path('', views.index, name='index'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

