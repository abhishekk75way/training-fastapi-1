# FastAPI Production Backend

## Overview

This project is a setup for practical FastAPI backend development with production-ready features like dependency injection, role-based access control, and database migrations. It is designed for scalability, maintainability, and real-world usage in SaaS platforms, authentication services, and microservice architectures.

### Technology Stack

* **FastAPI** – High-performance asynchronous web framework
* **SQLModel** – ORM built on SQLAlchemy with Pydantic integration
* **Pydantic v2** – Data validation and serialization
* **Alembic** – Database migrations and schema versioning
* **PostgreSQL** – Primary database (MySQL / SQLite supported)
* **JWT (python-jose)** – Stateless authentication
* **RBAC** – Role-Based Access Control
* **Passlib (bcrypt)** – Secure password hashing
* **CORS Middleware** – Frontend communication support
* **FastAPI Dependency Injection** – Modular and testable design

## Core Features

### Authentication

* User registration and login
* JWT-based access tokens
* Secure password hashing using bcrypt
* Configurable token expiration

### Role-Based Access Control (RBAC)

* Built-in roles: `user`, `admin`
* Role embedded inside JWT payload
* Route-level role protection

Role behavior:

```
user  -> limited access
admin -> full access
```

## Project Architecture

```
API Routes
   ↓
Services (Business Logic)
   ↓
Repositories (Database Access)
   ↓
Database (SQLModel)
```

### Architectural Benefits

* Clear separation of concerns
* High testability
* Easy scalability
* Industry-standard backend structure

## Dependency Injection

FastAPI dependencies are used extensively for:

* Database session management
* Authentication and authorization
* Role validation

Example usage:

```python
Depends(get_session)
Depends(get_current_user)
```

## Security

### Password Management

* Passwords are hashed using bcrypt
* Plain-text passwords are never stored

### JWT Payload Structure

```json
{
  "sub": "user_id",
  "role": "user",
  "exp": 1700000000
}
```

## Middleware

### CORS Configuration

CORS middleware enables frontend applications (React, Next.js, mobile apps) to communicate with the backend API.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Authentication Handling

* JWT validation is handled via FastAPI dependencies
* Middleware-based authentication can be added if required

## Database Layer

### SQLModel

* Combines SQLAlchemy ORM with Pydantic validation
* Type-safe and developer-friendly models

### Alembic Migrations

Generate and apply migrations:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head

alembic downgrade -1 # one step back
alembic downgrade base # to the very first migration
```

## Environment Configuration

Create a `.env` file at the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET=supersecretkey
```

## Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003
http://localhost:8003 # Run the application
```

### API Documentation

* Swagger UI: [http://localhost:8003/docs](http://localhost:8003/docs)
