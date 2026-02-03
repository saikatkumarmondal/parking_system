from django.db import models
from django.utils import timezone
from datetime import timedelta

class Zone(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Slot(models.Model):
    STATUS_CHOICES = [('available', 'Available'), ('occupied', 'Occupied')]
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='slots')
    slot_code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.slot_code

class Device(models.Model): 
    HEALTH_CHOICES = [
        ('Healthy', 'Healthy'),
        ('Warning', 'Warning'),
        ('Critical', 'Critical'),
        ('Offline', 'Offline'),
    ]
    device_code = models.CharField(max_length=50, unique=True)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE, related_name='device')
    name = models.CharField(max_length=100)
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='Healthy')
    last_reported = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_code} ({self.health_status})"

    
    def update_heartbeat_status(self):
        if not self.last_reported:
            return "Offline"
        
        diff = timezone.now() - self.last_reported
        if diff > timedelta(minutes=10):
            self.health_status = 'Offline'
        elif diff > timedelta(minutes=2):
            self.health_status = 'Warning'
       
        self.save()

class TelemetryData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetry_logs')
    voltage = models.FloatField()
    current = models.FloatField()
    power_factor = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
      
        new_status = "Healthy"
        
        if self.voltage > 250 or self.voltage < 180:
            new_status = "Critical"
        elif self.power_factor < 0.8:
            new_status = "Warning"
            
        
        self.device.health_status = new_status
        self.device.save() 
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
        # Requirement 5.4 & 6.3: Duplicate handling (Same device + timestamp)
        unique_together = ('device', 'timestamp')