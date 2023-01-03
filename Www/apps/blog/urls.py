from django.urls import path
from django.views.generic import TemplateView

from .views import index

urlpatterns = [
    path('', index, name="index"),
]
