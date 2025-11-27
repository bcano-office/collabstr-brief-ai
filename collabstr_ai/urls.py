"""
URL configuration for collabstr_ai project.
"""
from django.contrib import admin
from django.urls import path
from brief_generator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/generate-brief/', views.generate_brief, name='generate_brief'),
    path('', views.index, name='index'),
]

