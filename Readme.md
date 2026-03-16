# Nexora Bot

Nexora Bot is a **Multi-Modal RAG (Retrieval-Augmented Generation)** system that enables document ingestion, embedding generation, and semantic retrieval using modern AI tooling.

The platform combines a scalable backend with asynchronous processing and a modern frontend.

## Core Technologies

* **FastAPI** - Backend API
* **Celery** - Asynchronous task processing
* **Redis** - Message broker for Celery
* **Supabase** - Cloud PostgreSQL + storage
* **Next.js** - Frontend application
* **Clerk** - Authentication provider
* **Docker** - Backend containerization

The repository contains both the **frontend** and **backend infrastructure** required to run the system locally.

---

# Project Structure

```
NEXORABOT/
│
├── Nexora_Bot_Client/        # Next.js Frontend
│   ├── src/
│   ├── public/
│   ├── .env.example
│   └── package.json
│
└── Nexora_Bot_Server/        # Dockerized Backend
    ├── src/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── pyproject.toml
    ├── poetry.lock
    ├── .env.docker.example
    └── supabase/
        └── migrations/
```

---

# Architecture

```
Next.js Frontend
        │
        ▼
FastAPI Backend (Docker)
        │
        ▼
Redis Queue
        │
        ▼
Celery Worker
        │
        ▼
Supabase (PostgreSQL + Storage)
```

Key system responsibilities:

| Component     | Responsibility            |
| ------------- | ------------------------- |
| Frontend      | User interface            |
| FastAPI       | API layer                 |
| Redis         | Task queue broker         |
| Celery Worker | Background ingestion jobs |
| Supabase      | Database + storage        |

---

# Prerequisites

Ensure the following tools are installed before running the project:

* Docker Desktop
* Node.js 18+
* A Supabase Cloud project
* A Clerk authentication project


---

# Environment Configuration

## Backend

Navigate to:

```
Nexora_Bot_Server/
```

Create:

```
.env.docker
```

Use `.env.docker.example` as reference.

Important variables:

```
SUPABASE_API_URL=
SUPABASE_SECRET_KEY=
DATABASE_URL=
CLERK_SECRET_KEY=
DOMAIN=
REDIS_URL=redis://redis:6379
```

Notes:

* `SUPABASE_SECRET_KEY` must be the **service role key**.
* `DATABASE_URL` should use the **Supabase Session Pooler endpoint**.

Example:

```
postgresql://postgres:PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Remove any extra query parameters such as `pgbouncer=true`.

---

## Frontend

Navigate to:

```
Nexora_Bot_Client/
```

Create:

```
.env
```

Use `.env.example` as reference.

Example variables:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

# Database Migrations

The backend automatically runs SQL migrations during startup.

Migration files are located in:

```
supabase/migrations/
```

These migrations create:

* database tables
* indexes
* search functions
* permissions

A migration runner executes these files in order.

To reset the database during development:

```sql
drop schema public cascade;
create schema public;
```

After resetting, restart the backend containers and migrations will run again.

---

# Running the Project

## Start Backend

```bash
cd Nexora_Bot_Server
docker compose up --build
```

This launches:

* FastAPI backend
* Celery worker
* Redis broker

Verify the backend:

```
http://localhost:8000/docs
```

---

## Start Frontend

In a separate terminal:

```bash
cd Nexora_Bot_Client
npm install
npm run dev
```

Frontend will be available at:

```
http://localhost:3000
```

---

# Stopping the Backend

```bash
cd Nexora_Bot_Server
docker compose down
```

---

# Running Backend Using Prebuilt Docker Image

Prebuilt image is available on Docker Hub, the backend can be started without building locally.

```
docker pull safibaig03/nexora-api:latest
```

Then run:

```
docker compose up
```

---

# Important Notes

* Backend is fully containerized.
* Redis runs inside Docker.
* Supabase is cloud hosted.
* Celery processes ingestion tasks asynchronously.
* First build may take several minutes due to ML dependencies.
* Docker should have **at least 8GB RAM allocated**.

---


# Development Notes

During development you may need to reset the database or rerun migrations.

Common workflow:

```
reset supabase schema
↓
docker compose up
↓
migrations run automatically
```

---

# Summary

Nexora Bot provides a full **AI-powered RAG platform** with:

* scalable API
* asynchronous ingestion
* modern frontend
* cloud database

The Dockerized backend and migration system allow the entire stack to be reproduced easily on any machine.
