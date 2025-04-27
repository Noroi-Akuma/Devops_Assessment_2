from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import datetime
import logging

# Define the application version and fetch the hostname from environment variables
APP_VERSION = "1.0.0"
HOSTNAME = os.environ.get("HOSTNAME", "unknown")


# Set up logging with a custom format
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Create the FastAPI app instance
app = FastAPI(title="DevOps Assignment 2 - Practical Part", version=APP_VERSION)

# Class to store the application state
class AppState:
    def __init__(self):
        self.request_counter = 0
        self.started_at = datetime.datetime.now()

# Initialize global state
state = AppState()

# Utility function to compute uptime in seconds
def compute_uptime() -> float:
    return (datetime.datetime.now() - state.started_at).total_seconds()

# Pydantic model for a structured response
class StatusResponse(BaseModel):
    message: str
    host: str
    version: str
    request_count: int
    uptime_seconds: float
    timestamp: str

# Define the root endpoint with a distinct response
@app.get("/", response_model=StatusResponse, summary="Get app status")
async def root_status():
    state.request_counter += 1
    uptime = compute_uptime()
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Assemble the response data
    response = StatusResponse(
        message="Hello from your DevOps Coursework 2 app!",
        host=HOSTNAME,
        version=APP_VERSION,
        request_count=state.request_counter,
        uptime_seconds=uptime,
        timestamp=current_timestamp,
    )
    
    # Log the request details with a distinct format
    logging.info(
        f"Host: {HOSTNAME} | Requests: {state.request_counter} | Uptime: {uptime:.2f}s"
    )
    
    return response


@app.on_event("startup")
async def startup_event():
    logging.info(f"Server started at {state.started_at} on host {HOSTNAME}")

# Main entry point to start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
