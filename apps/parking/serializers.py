from rest_framework import serializers
from .models import Zone, Slot, Device, TelemetryData

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class DeviceSerializer(serializers.ModelSerializer):
    slot = serializers.SlugRelatedField(
        slug_field='slot_code', 
        queryset=Slot.objects.all()
    )

    class Meta:
        model = Device
        fields = '__all__'

class TelemetryDataSerializer(serializers.ModelSerializer):
    device = serializers.SlugRelatedField(
        slug_field='device_code', 
        queryset=Device.objects.all()
    )

    class Meta:
        model = TelemetryData
        fields = ['device', 'voltage', 'current', 'power_factor', 'timestamp']

    def create(self, validated_data):
        """
        Requirement 5.4: Implement duplicate handling.
        If a record with the same device and timestamp exists, 
        return that record instead of creating a new one.
        """
        instance, created = TelemetryData.objects.get_or_create(
            device=validated_data['device'],
            timestamp=validated_data['timestamp'],
            defaults=validated_data
        )
        return instance