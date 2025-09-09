from django.urls import path
from .views import health, backends

urlpatterns = [
    path("health", health),
    path("backends",backends)
]
