🅿️ Smart Car Parking Monitoring SystemA full-stack monitoring solution designed to track car parking occupancy, historical telemetry (voltage/current), and device health in real-time.1. Project OverviewThis system allows facility operators to monitor parking zones, track individual slot statuses, and ensure that monitoring devices are functional. It is built using a Django REST Framework backend and a Neon DB (PostgreSQL) cloud database.2. Setup InstructionsPrerequisitesPython 3.12+Neon DB or any PostgreSQL instanceStep 1: Clone and Environment SetupBashgit clone https://github.com/saikatkumarmondal/parking_system
cd parking_system
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
Step 2: Install DependenciesBashpip install -r requirements.txt
Step 3: Configure Environment VariablesCreate a .env file in the root directory:Code snippetSECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://neondb_owner:123456@ep-cool-water.neon.tech/parking_db?sslmode=require
Step 4: Run Migrations and Seed DataBashpython manage.py migrate
python manage.py shell < generate_data.py
python manage.py runserver 3. API Documentation🔑 AuthenticationAll endpoints (except login) require a JWT Bearer Token.EndpointMethodDescription/api/auth/login/POSTGet access/refresh tokensCredentials:Username: adminPassword: 123456🏗️ Setup & ConfigurationUsed to initialize the facility structure.EndpointMethodPurpose/api/zones/POSTCreate a parking zone (e.g., Basement 1)/api/slots/POSTCreate a slot and link to a zone/api/devices/POSTRegister a new monitoring device📊 Monitoring & TelemetryUsed by IoT devices to send data and by the dashboard to read it.Device IngestionEndpoint: POST /api/telemetry/Payload:JSON{
"device_code": "DEV-101",
"voltage": 220.5,
"current": 5.2,
"power_factor": 0.92,
"timestamp": "2026-02-04T10:30:00Z"
}
Operator QueriesDashboard Summary: GET /api/dashboard/overview/ (Returns total/occupied/free slots)List Devices: GET /api/devices/Telemetry History: GET /api/telemetry/?device_code=DEV-101Date Filtering: GET /api/telemetry/?device_code=DEV-999&start_date=2026-02-01&end_date=2026-02-044. Key Business Logic (Assessment Requirements)Duplicate Handling (Requirement 5.4)The backend enforces a Unique Constraint on the combination of device_code and timestamp.Policy: If a duplicate packet is received, it is ignored (or rejected with a 400 error) to prevent corrupting historical usage analytics.Device Health Monitoring (Requirement 5.3)Health status is calculated based on the last heartbeat:🟢 Healthy: Last seen ≤ 2 minutes ago.🟡 Warning: Last seen between 2 and 10 minutes ago.🔴 Offline: Last seen > 10 minutes ago.5. AssumptionsDevice Pre-registration: Telemetry is only accepted from devices already registered in the system.Timezone: All timestamps are handled in UTC to ensure consistency across different sensor locations.Slot-Device Mapping: Each slot is mapped to exactly one device
