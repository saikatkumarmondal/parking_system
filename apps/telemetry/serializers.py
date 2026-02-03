from rest_framework import serializers
from .models import TelemetryData
from apps.parking.models import Device

class TelemetrySerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(write_only=True)

    class Meta:
        model = TelemetryData
        fields = ['device_code', 'voltage', 'current', 'power_factor', 'timestamp']

    def validate_device_code(self, value):
        # Rule: Device existence check
        if not Device.objects.filter(device_code=value).exists():
            raise serializers.ValidationError("This device is not registered in the system.")
        return value

    def create(self, validated_data):
        device_code = validated_data.pop('device_code')
        device = Device.objects.get(device_code=device_code)
        
        # Rule: Duplicate handling (Same device + timestamp)
        # update_or_create 
        obj, created = TelemetryData.objects.update_or_create(
            device=device,
            timestamp=validated_data.get('timestamp'),
            defaults=validated_data
        )
        return obj