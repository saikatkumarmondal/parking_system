from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeviceViewSet, 
    ZoneViewSet, 
    SlotViewSet, 
    TelemetryDataViewSet, 
    ParkingOverviewAPI
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'zones', ZoneViewSet, basename='zone')
router.register(r'slots', SlotViewSet, basename='slot') 
router.register(r'telemetry', TelemetryDataViewSet, basename='telemetry')

urlpatterns = [
    path('dashboard/overview/', ParkingOverviewAPI.as_view(), name='parking-overview'),
    path('', include(router.urls)),
]