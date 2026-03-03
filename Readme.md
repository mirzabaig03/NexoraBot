# Nexora Bot

Nexora Bot is a Multi-Modal RAG (Retrieval-Augmented Generation) application built with:

* **FastAPI** (Backend API)
* **Celery** (Asynchronous ingestion worker)
* **Redis** (Message broker)
* **Supabase Cloud** (Database + Storage)
* **Next.js** (Frontend)
* **Clerk** (Authentication)

This repository contains both the frontend and the fully containerized backend.

---

# 🏗 Project Structure

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
```

---

# 🧱 Architecture Overview

```
Frontend (Next.js)
        ↓
FastAPI Backend (Docker)
        ↓
Redis (Docker)
        ↓
Celery Worker (Docker)
        ↓
Supabase Cloud
```

---

# ⚙️ Prerequisites

Make sure the following are installed:

* **Docker Desktop** (required)
* **Node.js 18+**
* A **Supabase Cloud project**
* A **Clerk project** for authentication

No local PostgreSQL or Supabase installation is required.

---

# 🔐 Environment Configuration

## 1️⃣ Backend Configuration

Navigate to:

```
Nexora_Bot_Server/
```

Create a file named:

```
.env.docker
```

Use `.env.docker.example` as reference.

Example structure:

```env
CLERK_SECRET_KEY=
DOMAIN=http://localhost:3000/

SUPABASE_API_URL=
SUPABASE_SECRET_KEY=    # Supabase Service Role Key

REDIS_URL=redis://redis:6379/0

OPENAI_API_KEY=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_ENDPOINT_URL_S3=https://t3.storage.dev
AWS_REGION=auto
```

Important:

* `SUPABASE_SECRET_KEY` must be the **Service Role Key**.
* This file must NOT be committed.

---

## 2️⃣ Frontend Configuration

Navigate to:

```
Nexora_Bot_Client/
```

Create a file named:

```
.env
```

Use `.env.example` as reference.

Example:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Important:

* Do NOT add service role keys in the frontend.
* Only public keys should be exposed here.

---

# 🚀 Running the Project

## Step 1 — Start the Backend

Open a terminal and run:

```bash
cd Nexora_Bot_Server
docker compose up --build
```

This will start:

* FastAPI backend on **[http://localhost:8000](http://localhost:8000)**
* Celery worker
* Redis message broker

To verify backend is running, open:

```
http://localhost:8000/docs
```

---

## Step 2 — Start the Frontend

Open a new terminal and run:

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

# 🧪 Testing the Application

1. Open the frontend in your browser.
2. Sign in using Clerk authentication.
3. Upload a document.
4. Trigger ingestion.
5. The Celery worker will process the document asynchronously.

You can monitor worker logs using:

```bash
docker compose logs -f worker
```

---

# 🛑 Stopping the Backend

From inside `Nexora_Bot_Server/`:

```bash
docker compose down
```

---

# 📌 Important Notes

* Backend is fully containerized using Docker.
* Supabase is cloud-hosted.
* Redis runs inside Docker.
* Frontend runs locally using Node.js.
* First Docker build may take significant time due to ML dependencies.
* Ensure Docker has sufficient memory allocated (8GB recommended).

---

# 🔐 Security

* Backend uses Supabase **Service Role Key** for system-level operations.
* Frontend must only use public keys.
* Never commit `.env` or `.env.docker` files.
* Rotate keys immediately if exposed.

---

This setup allows full local development and testing of the complete Nexora Bot system.
