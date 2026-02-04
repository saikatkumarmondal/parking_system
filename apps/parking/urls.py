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
    # Dashboard Summary API (Requirement 7.1)
    path('dashboard/overview/', ParkingOverviewAPI.as_view(), name='parking-overview'),
    
    # ViewSets Router include
    path('', include(router.urls)),
]