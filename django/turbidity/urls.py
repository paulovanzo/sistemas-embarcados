from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('turbidity/', views.sensor, name='teste-api'),
    path('prometheus/', include('django_prometheus.urls')),
]
