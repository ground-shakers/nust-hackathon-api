# Healthcare API 🏥

A comprehensive, modern healthcare management API built with FastAPI, designed to streamline healthcare services including patient management, appointment scheduling, medical diagnoses, and healthcare provider coordination.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Authentication & Authorization](#authentication--authorization)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Healthcare Management
- 👥 **Multi-Role User System**: Support for Patients, Doctors, Nurses, Administrators, and Pharmacists
- 📅 **Appointment Scheduling**: Complete appointment lifecycle with automated notifications
- 🔬 **AI-Enhanced Diagnostics**: Comprehensive diagnosis tracking with confidence levels
- 📋 **Patient Records**: Detailed medical histories, allergies, and insurance management
- 👨‍⚕️ **Healthcare Provider Profiles**: Doctor specialties, experience, and facility affiliations

### Advanced Technical Features
- 📱 **Real-time SMS Notifications**: Vonage-powered appointment confirmations
- 🛡️ **Rate Limiting**: Configurable API protection (5 requests/minute default)
- 🔒 **Idempotency Support**: Duplicate operation prevention with Redis caching
- 🎫 **JWT Authentication**: Scope-based permissions and secure session management
- 📊 **Comprehensive Logging**: Rotating file logs with configurable retention
- 🌐 **CORS Support**: Cross-origin resource sharing for web applications
- ⚡ **Background Tasks**: Asynchronous processing for non-blocking operations

## 🏗️ Architecture

```
Healthcare API
├── FastAPI Application Layer
│   ├── Authentication & Authorization (JWT + Scopes)
│   ├── Rate Limiting (Redis-based)
│   ├── CORS Middleware
│   └── Idempotency Middleware
├── Business Logic Layer
│   ├── User Management (5 Role Types)
│   ├── Appointment System
│   ├── Diagnosis Management
│   └── Notification System (SMS)
├── Data Access Layer
│   ├── MongoDB with Beanie ODM
│   ├── Redis for Caching & Rate Limiting
│   └── Pydantic Models for Validation
└── External Services
    ├── Vonage SMS API
    └── JWT Token Management
```

## 📋 Prerequisites

- **Python**: 3.13+
- **MongoDB**: 4.4+ (Local or Cloud instance)
- **Redis**: 6.0+ (For rate limiting and caching)
- **Vonage Account**: For SMS notifications (optional)

## 🚀 Installation

### 1. Clone the Repository
```cmd
git clone https://github.com/ground-shakers/nust-hackathon-api.git
cd nust-hackathon-api
```

### 2. Create Virtual Environment
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 4. Create Environment Configuration
Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_CONNECTION_STRING=mongodb://localhost:27017
DATABASE_NAME=healthcare_api

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Security Configuration
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Vonage SMS Configuration (Optional)
VONAGE_API_KEY=your-vonage-api-key
VONAGE_API_SECRET=your-vonage-api-secret
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_CONNECTION_STRING` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `DATABASE_NAME` | MongoDB database name | `healthcare_api` | Yes |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` | Yes |
| `SECRET_KEY` | JWT signing secret | None | Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` | Yes |
| `VONAGE_API_KEY` | Vonage SMS API key | None | No |
| `VONAGE_API_SECRET` | Vonage SMS API secret | None | No |

### Logging Configuration

Logs are automatically configured with:
- **File**: `logs/healthcare_api.log` (10MB rotation, 5 backups)
- **Console**: Real-time output during development
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## 🏃‍♂️ Running the Application

### Development Mode
```cmd
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```cmd
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **ReDoc**: `http://localhost:8000/redoc`

## 📚 API Documentation

### Interactive Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## 🗄️ Database Models

### User Models
- **Patient**: Medical history, allergies, insurance, appointments
- **Doctor**: Specialties, experience, medical facility, reviews
- **Nurse**: Department, experience, affiliated facilities
- **Admin**: System administration capabilities
- **Pharmacist**: Pharmacy affiliation and drug inventory access

### Medical Models
- **Appointment**: Patient-doctor scheduling with status tracking
- **Diagnosis**: AI-enhanced diagnostic records with confidence levels
- **Treatment**: Medication prescriptions and treatment plans
- **Medical Facilities**: Hospitals, clinics, and pharmacies

### Supporting Models
- **Drug & Inventory**: Medication tracking and availability
- **Contact Info**: Email and phone validation
- **Reviews**: Rating system for healthcare providers

## 🔐 Authentication & Authorization

### JWT Token Structure
```json
{
  "sub": "user@email.com",
  "scopes": ["me", "get-patient", "get-appointments"],
  "exp": 1640995200
}
```

### Available Scopes
- `me`: Access own user information
- `admin`: Administrative privileges
- `get-patient`: Access patient information
- `get-patients`: Access all patients (healthcare providers)
- `get-doctor`: Access doctor information
- `get-appointment`: Access appointment information

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (@$!%*?&#)
- Cannot contain first or last name

## 🛣️ API Endpoints

### Authentication
```http
POST /login
```

### Patient Management
```http
POST   /api/v1/patients           # Create patient
GET    /api/v1/patients/{id}      # Get patient by ID
GET    /api/v1/patients           # List patients (paginated)
```

### Doctor Management
```http
POST   /api/v1/doctors            # Create doctor
GET    /api/v1/doctors/{id}       # Get doctor by ID
GET    /api/v1/doctors            # List doctors (paginated)
```

### Appointment Management
```http
POST   /api/v1/appointments       # Schedule appointment
GET    /api/v1/appointments/{id}  # Get appointment by ID
GET    /api/v1/appointments       # List appointments (filtered, paginated)
```

### Diagnosis Management
```http
POST   /api/v1/diagnoses          # Create diagnosis
GET    /api/v1/diagnoses/{id}     # Get diagnosis by ID
GET    /api/v1/diagnoses          # List diagnoses (filtered, paginated)
```

### Query Parameters

Most list endpoints support:
- `skip`: Number of records to skip (pagination)
- `limit`: Maximum records to return (max 100)
- `doctor_id`: Filter by doctor ID (appointments)
- `patient_id`: Filter by patient ID (appointments, diagnoses)

## 🧪 Testing

### Run Tests
```cmd
pytest
```

### Test Coverage
```cmd
pytest --cov=. --cov-report=html
```

### Manual API Testing

Use the interactive documentation at `/docs` or tools like:
- **Postman**: Import OpenAPI spec from `/openapi.json`
- **HTTPie**: Command-line HTTP client
- **curl**: Standard HTTP requests

Example patient creation:
```bash
curl -X POST "http://localhost:8000/api/v1/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "contact_info": {
      "email": "john.doe@email.com",
      "phone": "+1234567890"
    },
    "password": "SecurePass123!",
    "verify_password": "SecurePass123!",
    "gender": "male",
    "birthDetails": {
      "day": 15,
      "month": 8,
      "year": 1990
    }
  }'
```

## 🚀 Deployment

### Docker Deployment

1. **Create Dockerfile**:
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Run**:
```cmd
docker build -t healthcare-api .
docker run -p 8000:8000 --env-file .env healthcare-api
```

### Production Considerations

- Use environment variables for all configuration
- Set up MongoDB replica sets for high availability
- Configure Redis clustering for scalability
- Implement proper logging and monitoring
- Use reverse proxy (Nginx) for SSL termination
- Set up health check endpoints
- Configure rate limiting based on usage patterns

## 🆘 Support & Contact
- **Documentation**: [API Docs](https://ground-shakers.com/docs)

## 🙏 Acknowledgments

- **FastAPI**: For the excellent web framework
- **MongoDB**: For flexible document storage
- **Vonage**: For reliable SMS services
- **Redis**: For high-performance caching

---

**Built with ❤️ for better healthcare management by Ground Shakers**