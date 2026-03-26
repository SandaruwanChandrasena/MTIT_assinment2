# run_all.py
# Starts ALL microservices and API Gateway with a single command
# Run this file from the root folder:
# python run_all.py

import subprocess
import sys
import os
import time

# Get the root directory path
root_dir = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────
# SERVICE CONFIGURATION
# Define all services with folder and port
# ─────────────────────────────────────────
services = [
    {
        "name":   "Hotel Service",
        "folder": "hotel-service",
        "port":   8001
    },
    {
        "name":   "Room Service",
        "folder": "room-service",
        "port":   8002
    },
    {
        "name":   "Guest Service",
        "folder": "guest-service",
        "port":   8003
    },
    {
        "name":   "Booking Service",
        "folder": "booking-service",
        "port":   8004
    },
    {
        "name":   "Payment Service",
        "folder": "payment-service",
        "port":   8005
    },
    {
        "name":   "API Gateway",
        "folder": "api-gateway",
        "port":   8000
    },
]

processes = []

print("=" * 55)
print("   🏨 Hotel Booking System - Starting All Services")
print("=" * 55)

# Start each service as a separate process
for service in services:
    folder_path = os.path.join(root_dir, service["folder"])

    # Start the service using uvicorn
    process = subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--port", str(service["port"])
        ],
        cwd=folder_path  # Run from the service folder
    )

    processes.append(process)
    print(f"✅ {service['name']:<20} → port {service['port']}")
    time.sleep(1)  # Small delay between each service start

print("=" * 55)
print("\n📄 Direct Swagger URLs:")
print("   Hotel Service   → http://localhost:8001/docs")
print("   Room Service    → http://localhost:8002/docs")
print("   Guest Service   → http://localhost:8003/docs")
print("   Booking Service → http://localhost:8004/docs")
print("   Payment Service → http://localhost:8005/docs")
print("   API Gateway     → http://localhost:8000/docs")

print("\n🌐 Access via API Gateway:")
print("   Hotels    → http://localhost:8000/hotels")
print("   Rooms     → http://localhost:8000/rooms")
print("   Guests    → http://localhost:8000/guests")
print("   Bookings  → http://localhost:8000/bookings")
print("   Payments  → http://localhost:8000/payments")

print("\n⛔ Press CTRL+C to stop all services")
print("=" * 55)

# Keep running until CTRL+C
try:
    for process in processes:
        process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Stopping all services...")
    for process in processes:
        process.terminate()
    print("✅ All services stopped successfully!")
