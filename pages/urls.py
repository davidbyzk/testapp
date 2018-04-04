from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]