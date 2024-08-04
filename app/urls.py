from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('export-playlist/', views.export_playlist, name='export_playlist'),
    path('import-playlist/', views.import_playlist, name='import_playlist'),
]
