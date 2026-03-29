# API Gateway - Main Entry Point
# Single entry point for all microservices

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(
    title="API Gateway",
    description="Gateway for Hotel Booking System - Routes requests to microservices",
    version="1.0.0"
)

# ─────────────────────────────────────────
# CORS MIDDLEWARE
# Allows the React frontend (port 5173) to call this API
# Without this, the browser blocks cross-origin requests
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
# DYNAMIC CATCH-ALL ROUTES
# Handles all services with two routes
# ─────────────────────────────────────────
@app.api_route("/{service}", methods=["GET", "POST"])
async def service_root(service: str, request: Request):
    return await forward_request(request, service)

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def service_with_path(service: str, path: str, request: Request):
    return await forward_request(request, service, path)
