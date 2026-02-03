🅿️ Smart Car Parking Monitoring System

A full-stack parking monitoring solution designed to track parking occupancy, historical telemetry (voltage/current), and device health in real time.

The system enables facility operators to monitor parking zones, track individual slot statuses, and ensure all monitoring devices are functioning correctly.

🚀 Project Overview

This application is built with:

Backend: Django REST Framework

Database: Neon DB (PostgreSQL cloud)

Authentication: JWT-based authentication

Use Case: Smart parking facilities, IoT-based monitoring systems

Key capabilities include:

Real-time device health monitoring

Historical telemetry data tracking

Parking zone & slot management

Secure API access using JWT

⚙️ Setup Instructions
Prerequisites

Python 3.12+

PostgreSQL (Neon DB recommended)

Step 1: Clone Repository & Setup Virtual Environment
git clone https://github.com/saikatkumarmondal/parking_system
cd parking_system

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
Step 2: Install Dependencies
pip install -r requirements.txt
Step 3: Configure Environment Variables

Create a .env file in the project root:

SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://neondb_owner:123456@ep-cool-water.neon.tech/parking_db?sslmode=require
Step 4: Run Migrations & Seed Sample Data
python manage.py migrate
python manage.py shell < generate_data.py
python manage.py runserver


The server will start at:

http://127.0.0.1:8000

🔑 API Documentation
Authentication

All endpoints (except login) require a JWT Bearer Token.

Login Endpoint

POST /api/auth/login/


Credentials (Demo):

Username: admin

Password: 123456

🏗️ Setup & Configuration APIs

Used to initialize the parking facility structure.

Endpoint	Method	Description
/api/zones/	POST	Create a parking zone (e.g., Basement 1)
/api/slots/	POST	Create a slot and assign it to a zone
/api/devices/	POST	Register a new monitoring device
📊 Monitoring & Telemetry
Device Telemetry Ingestion

Endpoint

POST /api/telemetry/


Payload Example

{
  "device_code": "DEV-101",
  "voltage": 220.5,
  "current": 5.2,
  "power_factor": 0.92,
  "timestamp": "2026-02-04T10:30:00Z"
}

Operator / Dashboard APIs
Feature	Endpoint
Dashboard Overview	GET /api/dashboard/overview/
List All Devices	GET /api/devices/
Telemetry History	GET /api/telemetry/?device_code=DEV-101
Date Filtered Telemetry	GET /api/telemetry/?device_code=DEV-999&start_date=2026-02-01&end_date=2026-02-04
🧠 Key Business Logic (Assessment Requirements)
Duplicate Telemetry Handling (Requirement 5.4)

A unique constraint is enforced on:

(device_code, timestamp)


Policy:

Duplicate telemetry packets are ignored or rejected with a 400 Bad Request

This ensures historical analytics remain accurate

Device Health Monitoring (Requirement 5.3)

Device health is calculated based on the last heartbeat timestamp:

🟢 Healthy: Last reported ≤ 2 minutes ago

🟡 Warning: Last reported between 2–10 minutes ago

🔴 Offline: Last reported > 10 minutes ago

📌 Assumptions

Device Pre-registration: Telemetry is accepted only from registered devices

Timezone: All timestamps are handled in UTC

Slot-Device Mapping: Each parking slot is mapped to exactly one device

👨‍💻 Author

Saikat Kumar Mondal
