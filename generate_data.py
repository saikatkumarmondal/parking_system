import os
import django
import random
import sys
from pathlib import Path
from datetime import timedelta
from django.utils import timezone


BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


try:
  
    from apps.parking.models import Device, TelemetryData
    print("Models imported from apps.parking")
except ImportError:
    print("Error: Could not find models in apps.parking. Please check if models exist there.")
    sys.exit()

def seed_data():
   
    device, _ = Device.objects.get_or_create(
        device_code="DEV-101",
        defaults={'name': 'Main Gate Sensor'} 
    )

    data_list = []
    now = timezone.now()
    
    print("Generating 50 records...")
    for i in range(50):
        timestamp = now - timedelta(hours=i*2)
        data_list.append(TelemetryData(
            device=device,
            
            temperature=random.uniform(20.0, 30.0), 
            timestamp=timestamp
        ))
    
    TelemetryData.objects.bulk_create(data_list)
    print(f"Successfully added {len(data_list)} records!")

if __name__ == "__main__":
    seed_data()