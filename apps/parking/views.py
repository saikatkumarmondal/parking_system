from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Device, Slot, Zone, TelemetryData
from .serializers import DeviceSerializer, ZoneSerializer, SlotSerializer, TelemetryDataSerializer

class ParkingOverviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "total_slots": Slot.objects.count(),
            "available_slots": Slot.objects.filter(status='available').count(),
            "occupied_slots": Slot.objects.filter(status='occupied').count(),
            "critical_devices": Device.objects.filter(health_status='Critical').count(),
            "warning_devices": Device.objects.filter(health_status='Warning').count(),
            "healthy_devices": Device.objects.filter(health_status='Healthy').count(),
        }
        return Response(data)

class SlotViewSet(viewsets.ModelViewSet):
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Slot.objects.all()
        # Requirement 5.1: Filter availability by zone
        zone_code = self.request.query_params.get('zone_code')
        if zone_code:
            queryset = queryset.filter(zone__code=zone_code)
        return queryset

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAuthenticated]

class TelemetryDataViewSet(viewsets.ModelViewSet):
    serializer_class = TelemetryDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Requirement 5.2: Historical Analysis Requirements
        Filter by device, start_date, and end_date
        """
        queryset = TelemetryData.objects.all()
        device_code = self.request.query_params.get('device_code')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if device_code:
            queryset = queryset.filter(device__device_code=device_code)
        
        if start_date and end_date:
            # Expected format: YYYY-MM-DD
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
            
        return queryset