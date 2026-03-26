# API Gateway - Main Entry Point
# Single entry point for all microservices

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(
    title="API Gateway",
    description="Gateway for Hotel Booking System - Routes requests to microservices",
    version="1.0.0"
)

# ─────────────────────────────────────────
# SERVICE REGISTRY
# ─────────────────────────────────────────
SERVICES = {
    "hotels":   "http://localhost:8001",
    "rooms":    "http://localhost:8002",
    "guests":   "http://localhost:8003",
    "bookings": "http://localhost:8004",
    "payments": "http://localhost:8005",
}

# ─────────────────────────────────────────
# HELPER FUNCTION
# Forward request to correct microservice
# ─────────────────────────────────────────
async def forward_request(request: Request, service: str, path: str = ""):
    """Forwards incoming request to the correct microservice"""

    # Check if service exists
    if service not in SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service}' not found. Available: {list(SERVICES.keys())}"
        )

    # Build target URL
    if path:
        target_url = f"{SERVICES[service]}/{service}/{path}"
    else:
        target_url = f"{SERVICES[service]}/{service}"

    # Get request body and params
    body   = await request.body()
    params = dict(request.query_params)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method  = request.method,
                url     = target_url,
                content = body,
                params  = params,
                headers = {"Content-Type": "application/json"},
                timeout = 10.0
            )
        return JSONResponse(
            content     = response.json(),
            status_code = response.status_code
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code = 503,
            detail      = f"Service '{service}' is not running"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code = 504,
            detail      = f"Service '{service}' timed out"
        )

# ─────────────────────────────────────────
# ROOT ENDPOINT
# ─────────────────────────────────────────
@app.get("/")
async def root():
    """Shows all available services"""
    return {
        "message": "Hotel Booking System - API Gateway",
        "available_services": list(SERVICES.keys()),
        "examples": [
            "GET /hotels",
            "GET /rooms",
            "GET /guests",
            "GET /bookings",
            "GET /payments"
        ]
    }

# ─────────────────────────────────────────
# HOTELS ROUTES
# ─────────────────────────────────────────
@app.get("/hotels", tags=["Hotels"])
async def get_hotels(request: Request):
    return await forward_request(request, "hotels")

@app.get("/hotels/{path}", tags=["Hotels"])
async def get_hotel(path: str, request: Request):
    return await forward_request(request, "hotels", path)

@app.post("/hotels", tags=["Hotels"])
async def create_hotel(request: Request):
    return await forward_request(request, "hotels")

@app.put("/hotels/{path}", tags=["Hotels"])
async def update_hotel(path: str, request: Request):
    return await forward_request(request, "hotels", path)

@app.delete("/hotels/{path}", tags=["Hotels"])
async def delete_hotel(path: str, request: Request):
    return await forward_request(request, "hotels", path)

# ─────────────────────────────────────────
# ROOMS ROUTES
# ─────────────────────────────────────────
@app.get("/rooms", tags=["Rooms"])
async def get_rooms(request: Request):
    return await forward_request(request, "rooms")

@app.get("/rooms/{path}", tags=["Rooms"])
async def get_room(path: str, request: Request):
    return await forward_request(request, "rooms", path)

@app.post("/rooms", tags=["Rooms"])
async def create_room(request: Request):
    return await forward_request(request, "rooms")

@app.put("/rooms/{path}", tags=["Rooms"])
async def update_room(path: str, request: Request):
    return await forward_request(request, "rooms", path)

@app.delete("/rooms/{path}", tags=["Rooms"])
async def delete_room(path: str, request: Request):
    return await forward_request(request, "rooms", path)

# ─────────────────────────────────────────
# GUESTS ROUTES
# ─────────────────────────────────────────
@app.get("/guests", tags=["Guests"])
async def get_guests(request: Request):
    return await forward_request(request, "guests")

@app.get("/guests/{path}", tags=["Guests"])
async def get_guest(path: str, request: Request):
    return await forward_request(request, "guests", path)

@app.post("/guests", tags=["Guests"])
async def create_guest(request: Request):
    return await forward_request(request, "guests")

@app.put("/guests/{path}", tags=["Guests"])
async def update_guest(path: str, request: Request):
    return await forward_request(request, "guests", path)

@app.delete("/guests/{path}", tags=["Guests"])
async def delete_guest(path: str, request: Request):
    return await forward_request(request, "guests", path)

# ─────────────────────────────────────────
# BOOKINGS ROUTES
# ─────────────────────────────────────────
@app.get("/bookings", tags=["Bookings"])
async def get_bookings(request: Request):
    return await forward_request(request, "bookings")

@app.get("/bookings/{path}", tags=["Bookings"])
async def get_booking(path: str, request: Request):
    return await forward_request(request, "bookings", path)

@app.post("/bookings", tags=["Bookings"])
async def create_booking(request: Request):
    return await forward_request(request, "bookings")

@app.put("/bookings/{path}", tags=["Bookings"])
async def update_booking(path: str, request: Request):
    return await forward_request(request, "bookings", path)

@app.delete("/bookings/{path}", tags=["Bookings"])
async def delete_booking(path: str, request: Request):
    return await forward_request(request, "bookings", path)

# ─────────────────────────────────────────
# PAYMENTS ROUTES
# ─────────────────────────────────────────
@app.get("/payments", tags=["Payments"])
async def get_payments(request: Request):
    return await forward_request(request, "payments")

@app.get("/payments/{path}", tags=["Payments"])
async def get_payment(path: str, request: Request):
    return await forward_request(request, "payments", path)

@app.post("/payments", tags=["Payments"])
async def create_payment(request: Request):
    return await forward_request(request, "payments")

@app.put("/payments/{path}", tags=["Payments"])
async def update_payment(path: str, request: Request):
    return await forward_request(request, "payments", path)

@app.delete("/payments/{path}", tags=["Payments"])
async def delete_payment(path: str, request: Request):
    return await forward_request(request, "payments", path)
