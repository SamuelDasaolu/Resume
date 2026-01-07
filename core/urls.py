from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('preview/', views.preview, name='preview'),
    path('portfolio/<slug:slug>/', views.project_detail, name='project_detail'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
]
