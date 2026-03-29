# Hotel Booking System — Microservices Architecture

A microservices-based Hotel Booking System with a React frontend, built with Python, FastAPI, SQLite, and React + Tailwind CSS.

---

## Project Info

| Field        | Details                          |
|-------------|----------------------------------|
| Module       | IT4020 - Modern Topics in IT     |
| Assignment   | Assignment 2                     |
| Year         | Year 4 Semester 1/2 - 2026       |
| Architecture | Microservices + API Gateway      |

---

## Group Members & Contributions

| Member   | Service          | Port | Branch          |
|----------|-----------------|------|-----------------|
| Member 1 | Hotel Service   | 8001 | Hotel-Service   |
| Member 2 | Room Service    | 8002 | Room-Service    |
| Member 3 | Guest Service   | 8003 | Guest-Service   |
| Member 4 | Booking Service | 8004 | Booking-Service |
| Member 5 | Payment Service | 8005 | Payment-Service |
| All      | API Gateway     | 8000 | main            |
| All      | React Frontend  | 5173 | main            |

---

## Tech Stack

| Technology   | Purpose                                    |
|-------------|-------------------------------------------|
| Python 3.11+ | Backend programming language              |
| FastAPI      | Web framework for REST APIs               |
| Uvicorn      | ASGI server to run FastAPI                |
| SQLAlchemy   | ORM for database operations               |
| SQLite       | Lightweight database (one per service)    |
| httpx        | HTTP client for inter-service calls       |
| Pydantic     | Data validation and request/response schemas |
| React        | Frontend UI framework                     |
| Tailwind CSS | Utility-first CSS styling                 |
| Axios        | HTTP client for frontend API calls        |
| Vite         | Frontend build tool and dev server        |

---

## Project Structure

```
MTIT_assinment2/
├── run_all.py               # Start all backend services at once
├── seed_data.py             # Populate all services with 50 dummy records each
├── README.md
├── .gitignore
│
├── api-gateway/             # API Gateway (port 8000)
│   ├── main.py              # Routes requests to correct microservice
│   └── requirements.txt
│
├── hotel-service/           # Hotel Service (port 8001)
│   ├── main.py              # App entry + health check
│   ├── routes.py            # API endpoints (CRUD + search/filter/pagination)
│   ├── service.py           # Business logic layer
│   ├── models.py            # Database table definition
│   ├── schemas.py           # Request/response validation
│   ├── database.py          # SQLite connection
│   └── requirements.txt
│
├── room-service/            # Room Service (port 8002) — validates hotel_id
│   ├── main.py
│   ├── routes.py            # Calls Hotel Service on create
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── guest-service/           # Guest Service (port 8003)
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── booking-service/         # Booking Service (port 8004) — validates guest + room
│   ├── main.py
│   ├── routes.py            # Calls Guest & Room services, updates room availability
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
├── payment-service/         # Payment Service (port 8005) — validates booking
│   ├── main.py
│   ├── routes.py            # Calls Booking Service on create
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── requirements.txt
│
└── frontend/                # React Frontend (port 5173)
    ├── package.json
    ├── vite.config.js
    ├── src/
    │   ├── main.jsx
    │   ├── App.jsx           # Router + page navigation
    │   ├── api/api.js        # All API calls via gateway
    │   ├── components/
    │   │   └── Navbar.jsx
    │   └── pages/
    │       ├── HotelsPage.jsx    # Full CRUD + search + filter + pagination
    │       ├── RoomsPage.jsx
    │       ├── GuestsPage.jsx
    │       ├── BookingsPage.jsx
    │       └── PaymentsPage.jsx
    └── ...
```

---

## Architecture Overview

```
                    React Frontend (port 5173)
                           │
                           ▼
                    API Gateway (port 8000)
                           │
          ┌────────────────┼────────────────────┐
          │                │                    │
          ▼                ▼                    ▼
    Hotel Service    Room Service         Guest Service
    (port 8001)      (port 8002)          (port 8003)
    hotels.db        rooms.db             guests.db
          ▲                ▲                    ▲
          │                │                    │
          │         Booking Service             │
          │         (port 8004)─────────────────┘
          │         bookings.db
          │                ▲
          │                │
          │         Payment Service
          │         (port 8005)
          │         payments.db
          │
          └── Room Service calls Hotel Service (validate hotel_id)
```

### Inter-Service Communication

| Service         | Calls              | Purpose                                      |
|----------------|--------------------|--------------------------------------------- |
| Room Service    | Hotel Service      | Verify hotel exists before creating a room    |
| Booking Service | Guest Service      | Verify guest exists before creating a booking |
| Booking Service | Room Service       | Verify room exists + is available             |
| Booking Service | Room Service       | Mark room as unavailable after booking        |
| Booking Service | Room Service       | Mark room as available after deleting booking |
| Payment Service | Booking Service    | Verify booking exists before creating payment |

---

## Setup Guide

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

## Running the Application

### Start Backend (Terminal 1)

```bash
source venv/bin/activate        # Mac/Linux
# OR
venv\Scripts\activate           # Windows

python3 run_all.py              # Mac/Linux
# OR
python run_all.py               # Windows
```

### Seed Dummy Data (Terminal 2, one-time only)

```bash
source venv/bin/activate        # Mac/Linux
python3 seed_data.py            # Creates 50 records per service (250 total)
```

### Start Frontend (Terminal 3)

```bash
cd frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

---

## API Endpoints

### Via API Gateway (Recommended)

| Service  | URL                           |
|----------|-------------------------------|
| Hotels   | http://localhost:8000/hotels   |
| Rooms    | http://localhost:8000/rooms    |
| Guests   | http://localhost:8000/guests   |
| Bookings | http://localhost:8000/bookings |
| Payments | http://localhost:8000/payments |

### Hotel Service — Advanced Endpoints

| Operation       | Method | Endpoint                | Notes                       |
|----------------|--------|-------------------------|-----------------------------|
| Get all hotels  | GET    | /hotels                 | Supports search/filter/pagination |
| Search by name  | GET    | /hotels?search=Hilton   |                             |
| Filter by city  | GET    | /hotels?city=Colombo    |                             |
| Filter by stars | GET    | /hotels?stars=5         |                             |
| Min rating      | GET    | /hotels?min_rating=4    |                             |
| Pagination      | GET    | /hotels?skip=0&limit=20 |                             |
| Get one hotel   | GET    | /hotels/{id}            |                             |
| Create hotel    | POST   | /hotels                 |                             |
| Full update     | PUT    | /hotels/{id}            | All fields required         |
| Partial update  | PATCH  | /hotels/{id}            | Only changed fields needed  |
| Delete hotel    | DELETE | /hotels/{id}            |                             |
| Health check    | GET    | /health                 | Returns service + DB status |

### Other Services — Standard CRUD

| Operation | Method | Endpoint          |
|-----------|--------|-------------------|
| Get All   | GET    | /{resource}       |
| Get One   | GET    | /{resource}/{id}  |
| Create    | POST   | /{resource}       |
| Update    | PUT    | /{resource}/{id}  |
| Delete    | DELETE | /{resource}/{id}  |

---

## Swagger UI (API Documentation)

Each service auto-generates interactive API docs:

| Service         | Swagger URL                   |
|----------------|-------------------------------|
| Hotel Service   | http://localhost:8001/docs     |
| Room Service    | http://localhost:8002/docs     |
| Guest Service   | http://localhost:8003/docs     |
| Booking Service | http://localhost:8004/docs     |
| Payment Service | http://localhost:8005/docs     |
| API Gateway     | http://localhost:8000/docs     |

---

## Database

Each service has its own isolated SQLite database (Database per Service pattern):

| Service         | Database File |
|----------------|---------------|
| Hotel Service   | hotels.db     |
| Room Service    | rooms.db      |
| Guest Service   | guests.db     |
| Booking Service | bookings.db   |
| Payment Service | payments.db   |

Database files are created automatically on first run and excluded from Git.

---

## Key Microservices Patterns Implemented

- **API Gateway Pattern** — Single entry point routing to all services
- **Database per Service** — Each service owns its own database
- **Inter-Service Communication** — Services validate data across boundaries via HTTP
- **Service Layer Pattern** — Separation of routes (HTTP) and business logic (Hotel Service)
- **Health Check Endpoint** — Service status monitoring (Hotel Service)
- **Input Validation** — Pydantic schemas with field-level constraints
- **Search, Filter & Pagination** — Advanced query support (Hotel Service)

---

## Stopping Services

```bash
Press CTRL+C in each terminal
```

---

## Notes

- All services must be running for inter-service communication to work
- SQLite .db files and venv/ are excluded from Git via .gitignore
- Frontend communicates exclusively through the API Gateway (port 8000)
- CORS is configured on the API Gateway to allow frontend requests
