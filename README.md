# 🏨 Hotel Booking System — Microservices Architecture

A microservices-based backend for a Hotel Booking System built with
Python, FastAPI, and SQLite.

---

## 📋 Project Info

| Field        | Details                          |
|-------------|----------------------------------|
| Module       | IT4020 - Modern Topics in IT     |
| Assignment   | Assignment 2                     |
| Year         | Year 4 Semester 1/2 - 2026       |
| Tech Stack   | Python, FastAPI, SQLite          |
| Architecture | Microservices + API Gateway      |

---

## 👥 Group Members & Contributions

| Member   | Service          | Port |
|----------|-----------------|------|
| Member 1 | Hotel Service   | 8001 |
| Member 2 | Room Service    | 8002 |
| Member 3 | Guest Service   | 8003 |
| Member 4 | Booking Service | 8004 |
| Member 5 | Payment Service | 8005 |
| All      | API Gateway     | 8000 |

---

## 📁 Project Structure
```
hotel-booking-system/
│
├── venv/                    ← Virtual environment
├── run_all.py               ← Run all services at once
├── .gitignore               ← Git ignore file
├── README.md                ← This file
│
├── api-gateway/
│   ├── main.py              ← Gateway routing logic
│   └── requirements.txt
│
├── hotel-service/
│   ├── main.py              ← App entry point
│   ├── routes.py            ← API endpoints
│   ├── models.py            ← Database models
│   ├── schemas.py           ← Request/Response schemas
│   ├── database.py          ← SQLite connection
│   └── requirements.txt
│
├── room-service/            ← Same structure
├── guest-service/           ← Same structure
├── booking-service/         ← Same structure
└── payment-service/         ← Same structure
```

---

## 🛠️ Tech Stack

| Technology   | Purpose                        |
|-------------|-------------------------------|
| Python 3.11  | Programming language           |
| FastAPI      | Web framework for building APIs|
| Uvicorn      | ASGI server to run FastAPI     |
| SQLAlchemy   | ORM for database operations    |
| SQLite       | Lightweight database           |
| httpx        | HTTP client for API Gateway    |
| Pydantic     | Data validation and schemas    |

---

## ⚙️ Setup Guide

### Step 1 — Clone the Repository
```bash
git clone [<your-repo-url>](https://github.com/SandaruwanChandrasena/MTIT_assinment2.git)
cd hotel-booking-system
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
python -m pip install fastapi uvicorn sqlalchemy httpx
```

---

## ▶️ Running the Services

### Option 1 — Run ALL services at once (Recommended)
```bash
python run_all.py
```

### Option 2 — Run each service separately

Open separate terminals for each service:

**Terminal 1 — Hotel Service**
```bash
cd hotel-service
uvicorn main:app --reload --port 8001
```

**Terminal 2 — Room Service**
```bash
cd room-service
uvicorn main:app --reload --port 8002
```

**Terminal 3 — Guest Service**
```bash
cd guest-service
uvicorn main:app --reload --port 8003
```

**Terminal 4 — Booking Service**
```bash
cd booking-service
uvicorn main:app --reload --port 8004
```

**Terminal 5 — Payment Service**
```bash
cd payment-service
uvicorn main:app --reload --port 8005
```

**Terminal 6 — API Gateway**
```bash
cd api-gateway
uvicorn main:app --reload --port 8000
```

---

## 🌐 API Endpoints

### Access Directly

| Service         | URL                          |
|----------------|------------------------------|
| Hotel Service   | http://localhost:8001/hotels  |
| Room Service    | http://localhost:8002/rooms   |
| Guest Service   | http://localhost:8003/guests  |
| Booking Service | http://localhost:8004/bookings|
| Payment Service | http://localhost:8005/payments|

### Access via API Gateway

| Service         | URL                           |
|----------------|-------------------------------|
| Hotels          | http://localhost:8000/hotels  |
| Rooms           | http://localhost:8000/rooms   |
| Guests          | http://localhost:8000/guests  |
| Bookings        | http://localhost:8000/bookings|
| Payments        | http://localhost:8000/payments|

---

## 📄 Swagger UI (API Documentation)

### Direct Swagger URLs

| Service         | Swagger URL                    |
|----------------|-------------------------------|
| Hotel Service   | http://localhost:8001/docs     |
| Room Service    | http://localhost:8002/docs     |
| Guest Service   | http://localhost:8003/docs     |
| Booking Service | http://localhost:8004/docs     |
| Payment Service | http://localhost:8005/docs     |
| API Gateway     | http://localhost:8000/docs     |

---

## 📊 CRUD Operations

Each service supports full CRUD:

| Operation | Method | Endpoint          |
|-----------|--------|-------------------|
| Get All   | GET    | /hotels           |
| Get One   | GET    | /hotels/{id}      |
| Create    | POST   | /hotels           |
| Update    | PUT    | /hotels/{id}      |
| Delete    | DELETE | /hotels/{id}      |

---

## 🔄 Architecture Overview
```
Client / Browser
       │
       ▼
API Gateway (port 8000)
       │
       ├──► Hotel Service   (8001) ──► hotels.db
       ├──► Room Service    (8002) ──► rooms.db
       ├──► Guest Service   (8003) ──► guests.db
       ├──► Booking Service (8004) ──► bookings.db
       └──► Payment Service (8005) ──► payments.db
```

---

## 🗄️ Database

Each service has its own SQLite database file:

| Service         | Database File  |
|----------------|----------------|
| Hotel Service   | hotels.db      |
| Room Service    | rooms.db       |
| Guest Service   | guests.db      |
| Booking Service | bookings.db    |
| Payment Service | payments.db    |

Database files are created automatically when
you run each service for the first time.

---

## ⛔ Stopping Services

If running with run_all.py:
```bash
Press CTRL+C
```

If running separately — press CTRL+C in each terminal.

---

## 📝 Notes

- Make sure all services are running before
  testing via API Gateway
- SQLite .db files are excluded from Git
- Virtual environment folder is excluded from Git
```

---

## 📁 Final Root Level Structure
```
hotel-booking-system/
│
├── venv/               ← NOT in git
├── .gitignore          ← ✅ NEW
├── README.md           ← ✅ NEW
├── run_all.py          ← ✅ Already done
│
├── api-gateway/
├── hotel-service/
├── room-service/
├── guest-service/
├── booking-service/
└── payment-service/
```

---

## ✅ Create These Files at Root Level
```
☐ .gitignore     ← paste .gitignore code
☐ README.md      ← paste README.md code
