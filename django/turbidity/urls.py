from django.contrib import admin
from django.urls import path
from ..turbidity import views

urlpatterns = [
    path('turbidity/', views.sensor, name='teste-api'),
]
