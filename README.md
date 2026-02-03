# 🅿️ Smart Car Parking Slot Monitoring System (Backend)

## 📌 Project Overview

This is a robust backend solution for a Smart Car Parking Monitoring System. It tracks parking slot occupancy in real-time using IoT device telemetry data. The system features device registration, secure data ingestion, health monitoring (heartbeat), and historical analysis.

## 🚀 Features

- **Device Management:** Register and list parking monitoring devices.
- **Telemetry Ingestion:** Secure API to receive voltage, current, power factor, and occupancy status.
- **Data Integrity:** Strict duplicate handling (same device + same timestamp prevention).
- **Health Monitoring:** Real-time health calculation (Healthy, Warning, Offline) based on heartbeat.
- **Security:** JWT-based authentication for all endpoints.
- **Data Seeding:** Custom script to populate the database for testing.

## 🛠️ Technology Stack

- **Framework:** Django 6.0.1 + Django REST Framework (DRF)
- **Database:** PostgreSQL (Cloud-hosted via **Neon DB**)
- **Authentication:** Simple JWT (JSON Web Token)
- **Environment Management:** `python-decouple`, `dj-database_url`

## 📂 Project Structure

```text
parking_system/
├── apps/
│   ├── parking/          # Core logic (Devices & Slots)
│   └── telemetry/        # Time-series data & health monitoring
├── core/                 # Settings, WSGI, ASGI, and URL routing
├── venv/                 # Virtual environment
├── .env                  # Secrets and configurations
├── manage.py             # Django command-line utility
└── generate_data.py      # Custom script for dummy data seeding



⚙️ Setup & Installation1. PrerequisitesPython 3.14+Neon DB (PostgreSQL) account2. Installation StepsBash# Clone the repository
git clone <your-repository-url>
cd parking_system

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter dj-database-url python-decouple
3. Database & Environment ConfigurationCreate a .env file in the root folder and add your Neon DB credentials:Code snippetSECRET_KEY=django-insecure-highly-secret-key-2026
DEBUG=True
DATABASE_URL=postgres://neondb_owner:<password>@<neon-host>/parking_db?sslmode=require
4. Apply Migrations & Seed DataBash# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed dummy data for testing
python generate_data.py
5. Run ServerBashpython manage.py runserver
🔌 API Endpoints ReferenceMethodEndpointDescriptionPOST/api/auth/login/Obtain JWT Access & Refresh tokensGET/api/dashboard/overview/Get total, free, and occupied slot countsGET/api/devices/List all registered parking devicesPOST/api/telemetry/Ingest new telemetry data (Requires Auth)Sample Telemetry PayloadJSON{
  "device_code": "PARK-B1-S005",
  "voltage": 220.5,
  "current": 5.2,
  "power_factor": 0.92,
  "timestamp": "2026-02-04T10:30:00Z"
}
🧠 Business Logic & AssumptionsDuplicate Prevention: The system enforces a unique constraint on (device, timestamp). If a device sends the same data twice, it is rejected to ensure data accuracy.Device Health Logic:Healthy: Heartbeat seen within 2 minutes.Warning: Heartbeat seen within 2–10 minutes.Offline: No heartbeat for > 10 minutes.Directory Injection: Used sys.path.insert in settings to keep a clean apps/ directory structure.👤 AuthorYour:Saikat Kumar Mondal
 NameAssessment: Full Stack Software Engineer (Intern)Year: 2026
```
