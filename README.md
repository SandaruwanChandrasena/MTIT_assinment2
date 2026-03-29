# 🏨 Hotel Booking System — Microservices Architecture

A microservices-based Hotel Booking System built with **Python FastAPI**, **SQLite**, and **React + Tailwind CSS**, developed as part of the IT4020 Modern Topics in IT module at SLIIT.

---

## 📋 Project Info

| Field | Details |
|---|---|
| Module | IT4020 - Modern Topics in IT |
| Assignment | Assignment 2 |
| Year | Year 4 Semester 1/2 — 2026 |
| Institution | Sri Lanka Institute of Information Technology (SLIIT) |
| Architecture | Microservices + API Gateway |
| Submission Deadline | 31.03.2026 |

---

## 👥 Group Members & Contributions

| Member | Service | Port | Branch |
|---|---|---|---|
| Member 1 | Hotel Service | 8001 | Hotel-Service |
| Member 2 | Room Service | 8002 | Room-Service |
| Member 3 | Guest Service | 8003 | Guest-Service |
| Member 4 | Booking Service | 8004 | Booking-Service |
| Member 5 | Payment Service | 8005 | Payment-Service |
| All | API Gateway | 8000 | main |
| All | React Frontend | 5173 | main |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Backend programming language |
| FastAPI | Web framework for REST APIs |
| Uvicorn | ASGI server to run FastAPI |
| SQLAlchemy | ORM for database operations |
| SQLite | Lightweight database (one per service) |
| httpx | HTTP client for inter-service communication |
| Pydantic | Data validation and request/response schemas |
| React | Frontend UI framework |
| Tailwind CSS | Utility-first CSS styling |
| Axios | HTTP client for frontend API calls |
| Vite | Frontend build tool and dev server |

---

## 📁 Project Structure

```
MTIT_assinment2/
├── run_all.py                  # Start all backend services at once
├── seed_data.py                # Populate all services with 50 dummy records each
├── README.md
├── .gitignore
│
├── api-gateway/                # API Gateway (port 8000)
│   ├── main.py                 # Routes requests to correct microservice
│   └── requirements.txt
│
├── hotel-service/              # Hotel Service (port 8001)
│   ├── main.py                 # App entry + health check
│   ├── routes.py               # API endpoints (CRUD + search/filter/pagination)
│   ├── service.py              # Business logic layer
│   ├── models.py               # Database table definition
│   ├── schemas.py              # Request/response validation
│   ├── database.py             # SQLite connection
│   └── requirements.txt
│
├── room-service/               # Room Service (port 8002) — validates hotel_id
│   ├── main.py
│   ├── routes.py               # Calls Hotel Service on room create
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── guest-service/              # Guest Service (port 8003)
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── booking-service/            # Booking Service (port 8004) — validates guest + room
│   ├── main.py
│   ├── routes.py               # Calls Guest & Room services, updates room availability
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── payment-service/            # Payment Service (port 8005) — validates booking
│   ├── main.py
│   ├── routes.py               # Calls Booking Service on payment create
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
└── frontend/                   # React Frontend (port 5173)
    ├── package.json
    ├── vite.config.js
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx             # Router + page navigation
    │   ├── api/api.js          # All API calls routed via API Gateway
    │   ├── components/
    │   │   └── Navbar.jsx
    │   └── pages/
    │       ├── HotelsPage.jsx  # Full CRUD + search + filter + pagination
    │       ├── RoomsPage.jsx
    │       ├── GuestsPage.jsx
    │       ├── BookingsPage.jsx
    │       └── PaymentsPage.jsx
    └── ...
```

---

## 🏗️ Architecture Overview

```
                    React Frontend (port 5173)
                             │
                             ▼
                    API Gateway (port 8000)
                    [Single Entry Point]
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
    Hotel Service      Room Service       Guest Service
    (port 8001)        (port 8002)        (port 8003)
    hotels.db          rooms.db           guests.db
          ▲                  ▲                  ▲
          │                  │                  │
          └──────── Booking Service ────────────┘
                    (port 8004)
                    bookings.db
                             ▲
                             │
                    Payment Service
                    (port 8005)
                    payments.db
```

### 🔗 Inter-Service Communication

| Service | Calls | Purpose |
|---|---|---|
| Room Service | Hotel Service | Verify hotel exists before creating a room |
| Booking Service | Guest Service | Verify guest exists before creating a booking |
| Booking Service | Room Service | Verify room exists and is available |
| Booking Service | Room Service | Mark room as **unavailable** after booking created |
| Booking Service | Room Service | Mark room as **available** after booking deleted |
| Payment Service | Booking Service | Verify booking exists before creating a payment |

---

## ⚙️ Setup Guide

### Step 1 — Clone the Repository

```bash
git clone https://github.com/SandaruwanChandrasena/MTIT_assinment2.git
cd MTIT_assinment2
```

### Step 2 — Create & Activate Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Backend Dependencies

```bash
pip install fastapi uvicorn sqlalchemy httpx requests
```

### Step 4 — Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

---

## 🚀 Running the Application

### Terminal 1 — Start All Backend Services

```bash
# Mac/Linux
source venv/bin/activate
python3 run_all.py

# Windows
venv\Scripts\activate
python run_all.py
```

This starts all 5 microservices and the API Gateway simultaneously.

### Terminal 2 — Seed Dummy Data (one-time only)

```bash
# Mac/Linux
source venv/bin/activate
python3 seed_data.py

# Windows
venv\Scripts\activate
python seed_data.py
```

Creates **250 records total** (50 per service), seeded in dependency order so all inter-service validations pass.

### Terminal 3 — Start Frontend

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🌐 API Endpoints

### Via API Gateway (port 8000) — Recommended

| Service | URL |
|---|---|
| Hotels | http://localhost:8000/hotels |
| Rooms | http://localhost:8000/rooms |
| Guests | http://localhost:8000/guests |
| Bookings | http://localhost:8000/bookings |
| Payments | http://localhost:8000/payments |

### Hotel Service — Advanced Endpoints

| Operation | Method | Endpoint | Notes |
|---|---|---|---|
| Get all hotels | GET | `/hotels` | Supports search, filter & pagination |
| Search by name | GET | `/hotels?search=Hilton` | Case-insensitive |
| Filter by city | GET | `/hotels?city=Colombo` | Case-insensitive |
| Filter by stars | GET | `/hotels?stars=5` | Exact match (1–5) |
| Min rating filter | GET | `/hotels?min_rating=4` | Greater than or equal |
| Pagination | GET | `/hotels?skip=0&limit=20` | Default: skip=0, limit=20 |
| Get one hotel | GET | `/hotels/{id}` | |
| Create hotel | POST | `/hotels` | |
| Full update | PUT | `/hotels/{id}` | All fields required |
| Partial update | PATCH | `/hotels/{id}` | Only changed fields needed |
| Delete hotel | DELETE | `/hotels/{id}` | |
| Health check | GET | `/health` | Returns service + DB status |

### Other Services — Standard CRUD

| Operation | Method | Endpoint |
|---|---|---|
| Get All | GET | `/{resource}` |
| Get One | GET | `/{resource}/{id}` |
| Create | POST | `/{resource}` |
| Update | PUT | `/{resource}/{id}` |
| Delete | DELETE | `/{resource}/{id}` |

---

## 📄 Swagger UI (Interactive API Docs)

Each FastAPI service auto-generates interactive documentation:

| Service | Direct Swagger URL | Via Gateway |
|---|---|---|
| Hotel Service | http://localhost:8001/docs | http://localhost:8000/hotels |
| Room Service | http://localhost:8002/docs | http://localhost:8000/rooms |
| Guest Service | http://localhost:8003/docs | http://localhost:8000/guests |
| Booking Service | http://localhost:8004/docs | http://localhost:8000/bookings |
| Payment Service | http://localhost:8005/docs | http://localhost:8000/payments |
| API Gateway | http://localhost:8000/docs | — |

---

## 🗄️ Database

Each service has its own **isolated SQLite database** (Database-per-Service pattern). No shared databases — services communicate only via HTTP.

| Service | Database File |
|---|---|
| Hotel Service | `hotel-service/hotels.db` |
| Room Service | `room-service/rooms.db` |
| Guest Service | `guest-service/guests.db` |
| Booking Service | `booking-service/bookings.db` |
| Payment Service | `payment-service/payments.db` |

> Database `.db` files are created automatically on first run and are excluded from Git via `.gitignore`.

---

## ✅ Microservices Patterns Implemented

| Pattern | Description |
|---|---|
| **API Gateway Pattern** | Single entry point (port 8000) routing to all services — avoids multiple ports |
| **Database per Service** | Each service owns its own isolated SQLite database |
| **Inter-Service Communication** | Services validate data across boundaries via HTTP using `httpx` |
| **Service Layer Pattern** | Hotel Service separates HTTP concerns (routes.py) from business logic (service.py) |
| **Health Check Endpoint** | `/health` endpoint on Hotel Service for service status monitoring |
| **Input Validation** | Pydantic schemas with field-level constraints and descriptive error messages |
| **Search, Filter & Pagination** | Advanced query support on Hotel Service with `skip`/`limit` pagination |
| **Availability Management** | Room availability automatically updated when bookings are created or deleted |

---

## ⛔ Stopping Services

Press `CTRL+C` in each terminal to stop the services.

---

## 📝 Notes

- All backend services must be running before using the frontend or running `seed_data.py`
- The frontend communicates **exclusively through the API Gateway** (port 8000) — never directly to microservices
- CORS is configured on the API Gateway to allow requests from the React frontend (port 5173)
- SQLite `.db` files and `venv/` are excluded from Git via `.gitignore`
- Seed data is created in dependency order: Hotels → Rooms → Guests → Bookings → Payments