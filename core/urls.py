from django.urls import path
from . import views
from .views import ProjectDetailView, ServiceDetailView

urlpatterns = [
    path('', views.index, name='homepage'),
    path('preview/', views.preview, name='preview'),
    path('portfolio/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail'),
]
