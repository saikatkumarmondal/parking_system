from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Device, Slot, Zone, TelemetryData
from .serializers import DeviceSerializer, ZoneSerializer, SlotSerializer, TelemetryDataSerializer
from django.utils import timezone
from datetime import timedelta

class ParkingOverviewAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        healthy_limit = now - timedelta(minutes=2)
        warning_limit = now - timedelta(minutes=10)

        data = {
            "total_slots": Slot.objects.count(),
            "available_slots": Slot.objects.filter(status='available').count(),
            "occupied_slots": Slot.objects.filter(status='occupied').count(),
            
            "healthy_devices": Device.objects.filter(last_seen__gte=healthy_limit).count(),
            "warning_devices": Device.objects.filter(last_seen__lt=healthy_limit, last_seen__gte=warning_limit).count(),
            "critical_devices": Device.objects.filter(last_seen__lt=warning_limit).count(),
        }
        return Response(data)

class SlotViewSet(viewsets.ModelViewSet):
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Slot.objects.all()
        zone_code = self.request.query_params.get('zone_code')
        if zone_code:
            # Added __iexact for case-insensitive matching
            queryset = queryset.filter(zone__code__iexact=zone_code)
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
        Fix: Added Case-Insensitive filtering and cleaned up date range logic.
        """
        queryset = TelemetryData.objects.all().order_by('-timestamp')
        device_code = self.request.query_params.get('device_code')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if device_code:
            # Use __iexact to handle cases like 'dev-001' vs 'DEV-001'
            queryset = queryset.filter(device__device_code__iexact=device_code)
        
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
            
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Requirement 5.4 & 6.2: Ingestion & Duplicate Handling
        """
        device_code = request.data.get('device_code')
        timestamp = request.data.get('timestamp')

        try:
            # Use __iexact here too for flexibility
            device = Device.objects.get(device_code__iexact=device_code)
        except Device.DoesNotExist:
            return Response({"error": "Device not registered"}, status=status.HTTP_400_BAD_REQUEST)

        # Duplicate handling
        if TelemetryData.objects.filter(device=device, timestamp=timestamp).exists():
            return Response({"message": "Duplicate telemetry ignored"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device=device)
            
            # Update heartbeat logic
            device.last_seen = timestamp or timezone.now()
            device.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)