from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.middleware import LoggingMiddleware
from routes.v1 import v1_router

app = FastAPI(
    title="FastAPI Training API",
    description="""
This is the API documentation for the FastAPI Training application.

## Features
* Authentication (Login/Register)
* Admin user management
* Notifications system
""",
    version="1.0.1",
    contact={
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(v1_router)