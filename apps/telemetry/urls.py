from django.urls import path
from .views import TelemetryIngestionView

urlpatterns = [
    path('telemetry/', TelemetryIngestionView.as_view(), name='telemetry-ingestion'),
]