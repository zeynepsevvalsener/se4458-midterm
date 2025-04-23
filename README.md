

# ✈️ Airline Ticketing API

A minimal **RESTful Airline Ticketing System** built with **FastAPI** + **SQLAlchemy** and currently **deployed on Render.com (no Docker required)**.  
The service supports user registration & login, JWT-secured endpoints for flight management and ticket operations, paging, and a simple check-in flow.

---

## 📌 Repository

> **Source Code**: <https://github.com/zeynepsevvalsener/se4458-midterm>  

## 🎥 Demo Video

A quick walkthrough of the main flows (register → login → CRUD flights → buy ticket → check-in):  
<https://youtu.be/COzPM5P6aeM>

---

## 📑 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Architecture & Design](#-architecture--design)
- [Data Model (ER Diagram)](#-data-model-er-diagram)
- [Getting Started (Local)](#-getting-started-local)
- [Deploying to Render](#-deploying-to-render)
- [API Reference](#-api-reference)
- [Assumptions](#-assumptions)
- [Known Issues & Future Work](#-known-issues--future-work)

---

## ✨ Features

| Capability  | Endpoint                                    | Notes                |
| ----------- | ------------------------------------------- | -------------------- |
| **Auth**    | `POST /api/v1/auth/register`                | create user          |
|             | `POST /api/v1/auth/login`                   | returns **JWT**      |
| **Flights** | `POST /api/v1/flights`                      | *admin only*         |
|             | `GET /api/v1/flights?skip=0&limit=10&…`     | filter & paging      |
| **Tickets** | `POST /api/v1/tickets`                      | buy ticket           |
|             | `POST /api/v1/tickets/checkin`              | assign seat          |
|             | `GET /api/v1/tickets/passengers?flight_id=` | passenger list       |

Interactive docs: `https://se4458-midterm.onrender.com/docs` (Swagger).

---

## 🗂 Project Structure

```text
├── .gitignore
├── AirlineDB.session.sql
└── airline-api
    ├── app/ …                      # FastAPI package
    ├── requirements.txt
    └── render.yaml                 # (optional) IaC blueprint
```

---

## 🛠 Tech Stack

- **Python 3.11** · FastAPI 0.115  
- **SQLAlchemy 2** ORM  
- **PostgreSQL** (Render add-on)  
- **Pydantic v2** data validation  
- **JWT** auth via `python-jose`  

---

## 🏗 Architecture & Design

```text
               +-----------+     JWT    +-------------+
HTTP ──▶  API  │  Routers  │ ─────────▶ │  Services   │
Request        +-----------+           +------+-------+
                                         |  SQLAlchemy
                                         v
                                 +-------------+
                                 │   Models    │
                                 +-------------+
```

---

## 📊 Data Model (ER Diagram)

```mermaid
erDiagram
    FLIGHTS {
        int id PK
        date date_from
        date date_to
        string airport_from
        string airport_to
        int duration
        int capacity
    }
    TICKETS {
        int id PK
        int flight_id FK
        string passenger_name
        string ticket_number
        string checked_in
    }
    USERS {
        int id PK
        string username
        string email
        string hashed_password
    }
    FLIGHTS ||--o{ TICKETS : "has"
```

---

## 🚀 Getting Started (Local)

```bash
# 1. Clone
git clone https://github.com/zeynepsevvalsener/se4458-midterm.git
cd airline-api

# 2. Virtual env
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install deps
pip install -r airline-api/requirements.txt

# 4. Env vars (example)
export DATABASE_URL="postgresql://user:pass@localhost:5432/airline"
export JWT_SECRET=topsecret
export ACCESS_TOKEN_EXPIRE_MINUTES=60

# 5. Run
uvicorn airline-api.app.main:app --reload
```

---

## ☁️ Deploying to Render

1. **Create a new Web Service**  
   - **Runtime**: *Python 3.11*  
   - **Build Command**: `pip install -r airline-api/requirements.txt`  
   - **Start Command**: `uvicorn airline-api.app.main:app --host 0.0.0.0 --port $PORT`

2. **Add a PostgreSQL database** via Render add-ons and grab the **Internal Database URL**.

3. **Environment variables**

   | Key | Example |
   |-----|---------|
   | `DATABASE_URL` | `postgresql://user:pass@host:5432/db` |
   | `JWT_SECRET` | `sup3rsecret` |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` |

   *(Render automatically injects `PORT`; bind to it—never hard-code.)*

4. **Deploy** → wait for “Service is live” and test `.../docs`.

> **No Dockerfile is needed**—Render runs the app directly in its Python environment.

---

## 📖 API Reference

Swagger UI → `https://se4458-midterm.onrender.com/docs`  

---

## ✅ Assumptions

1. One **admin** user is seeded (`admin` / `1234`).  
2. Seat numbers are sequential (`S0…Sn`).  
3. Payment is out of scope—ticket purchase succeeds if capacity allows.

---

## 🐞 Known Issues & Future Work

| Area    | Issue / Limitation              | Planned Fix                           |
| ------- | ------------------------------ | ------------------------------------- |
| Auth    | Tokens are **not** refreshable | Add refresh-token endpoint            |
| Flights | No date-overlap validation     | Enforce unique (route + date range)   |
| Tickets | Race when seats < 3            | Use DB row-level locking              |
| Ops     | No CI / CD                     | GitHub Actions + automatic Render deploy |

---
