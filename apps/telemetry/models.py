from django.db import models
from apps.parking.models import Device 

class TelemetryData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetry')
    voltage = models.FloatField()
    current = models.FloatField()
    power_factor = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('device', 'timestamp')
        ordering = ['-timestamp']