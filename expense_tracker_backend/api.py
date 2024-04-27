from django.urls import path
from health.views import (HealthCheck)

urls = [
    #! ========================== HEALTH APP API ========================== !#
    path('health/', HealthCheck),
]