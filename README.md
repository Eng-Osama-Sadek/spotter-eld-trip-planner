# 🚛 Spotter ELD Trip Planner

> **Full-stack truck trip planning with automatic FMCSA-compliant ELD log generation.**
> Django REST Framework + React · OSRM routing · Nominatim geocoding · Custom Hours-of-Service engine.

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

---

## 🌐 Live Demo

| Service | URL | Status |
|---|---|---|
| 🎨 **Frontend (React + Vite)** | [spotter-eld-frontend-ten.vercel.app](https://spotter-eld-frontend-ten.vercel.app) | ![Vercel](https://img.shields.io/badge/Vercel-Deployed-success) |
| 🚀 **Backend API (Django)** | [spotter-eld-backend-production.up.railway.app](https://spotter-eld-backend-production.up.railway.app) | ![Railway](https://img.shields.io/badge/Railway-Deployed-success) |
| 💚 **Health Check** | [/api/health/](https://spotter-eld-backend-production.up.railway.app/api/health/) | ✅ Live |
| 🗺️ **Trip Planning API** | [/api/trips/plan/](https://spotter-eld-backend-production.up.railway.app/api/trips/plan/) | ✅ Live |
| ⚙️ **Admin Panel** | [/admin/](https://spotter-eld-backend-production.up.railway.app/admin/) | ✅ Live |

### 🎬 Try it now

1. Open **[spotter-eld-frontend-ten.vercel.app](https://spotter-eld-frontend-ten.vercel.app)**
2. Fill in:
   - **Current Location:** `Chicago, IL`
   - **Pickup Location:** `St. Louis, MO`
   - **Dropoff Location:** `Dallas, TX`
   - **Current Cycle Used (Hours):** `0`
3. Click **Plan Trip**
4. Wait ~15 seconds → see the map, fuel stops, and ELD log sheets!

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [HOS Rules Engine](#-hos-rules-engine)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Author](#-author)
- [License](#-license)

---

## 🎯 Overview

Planning long-haul truck trips in the United States requires balancing **three critical constraints**:

1. **FMCSA Hours-of-Service (HOS) regulations** — strict daily driving limits, mandatory rest breaks, and weekly cycle caps.
2. **Fuel efficiency** — refueling at the right stops to minimize cost.
3. **Driver fatigue management** — producing legally compliant daily logs for DOT inspections.

The **Spotter ELD Trip Planner** solves all three in a single API call:

- Accepts **current location**, **pickup**, **dropoff**, and **current cycle hours used**.
- Computes the optimal route via OSRM (single call per leg).
- Simulates the trip against a **custom FMCSA HOS rules engine** (11-hour driving, 14-hour window, 30-minute break, 70-hour/8-day cycle, 34-hour restart).
- Renders **per-day ELD log sheets** as SVG, matching the official FMCSA paper log format.
- Recommends **fuel stops** from a dataset of 8,000+ US truckstops.

---

## ✨ Features

### Backend
- 🧮 **Custom HOS Rules Engine** — simulates FMCSA compliance per day:
  - 11-hour maximum driving
  - 14-hour driving window
  - 30-minute break after 8 cumulative driving hours
  - 70-hour / 8-day cycle limit
  - 34-hour restart
  - Automatic fuel stops every 1,000 miles
  - 1-hour pickup + 1-hour dropoff (on-duty, not driving)
- 🗺️ **Single-Call Routing** — one OSRM call per leg (2 calls total).
- 📍 **Smart Geocoding** — Nominatim with LRU + Django cache, rate-limit compliant.
- ⛽ **Fuel Station Corridor** — 8,000+ stations indexed with a **SciPy KD-Tree** for microsecond spatial lookups.
- ⚡ **Fast** — cold start ~15s (external APIs), cached repeat <200ms.
- 🐳 **Dockerized** — production-ready Dockerfile deployed on Railway.

### Frontend
- 🎨 **Modern UI** — Tailwind + clean slate/brand color palette.
- 🗺️ **Interactive Map** — Leaflet + React-Leaflet showing route, leg 1 (blue), leg 2 (green), and fuel stops.
- 📊 **Trip Summary Cards** — miles, days, cycle start/end.
- 📋 **SVG ELD Log Sheets** — pixel-accurate to the FMCSA paper form.
- 📱 **Responsive** — works on desktop, tablet, and mobile.
- ⚡ **Vite** — blazing-fast HMR in development.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│              Browser (React + Vite)                      │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ TripForm   │→ │  RouteMap    │→ │ ELDLogSheet xN  │   │
│  └────────────┘  └──────────────┘  └─────────────────┘   │
│         │              ▲                    ▲            │
│         ▼              │                    │            │
│   POST /api/trips/plan/  (JSON)              │            │
└────────────────────┬─────────────────────────┼────────────┘
                     │                         │
                     ▼                         │
┌──────────────────────────────────────────────────────────┐
│              Django REST Framework                       │
│  ┌──────────────────────────────────────────────────┐    │
│  │              PlanTripView                        │    │
│  └──┬─────────────────┬──────────────────┬──────────┘    │
│     │                 │                  │               │
│     ▼                 ▼                  ▼               │
│  ┌────────┐    ┌──────────┐    ┌──────────────────┐      │
│  │Geocoder│    │  OSRM    │    │  HOS Engine      │      │
│  │Nominatim│   │ Routing  │    │ (Rule Simulator) │      │
│  └───┬────┘    └────┬─────┘    └────────┬─────────┘      │
│      │              │                   │                │
│      ▼              ▼                   ▼                │
│  ┌──────────────────────────────────────────────┐        │
│  │          Fuel Corridor + KD-Tree             │        │
│  │       (8,000+ stations indexed)              │        │
│  └──────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Django 5.0 + Django REST Framework 3.15 |
| **Routing API** | [OSRM](http://project-osrm.org/) (free, no key) |
| **Geocoding** | [Nominatim](https://nominatim.org/) / OpenStreetMap |
| **Spatial Index** | SciPy `cKDTree` |
| **Data Processing** | Pandas + NumPy |
| **Cache** | Django LocMem (dev) / Redis (prod) |
| **Frontend** | React 18 + Vite 5 |
| **Styling** | TailwindCSS 3 |
| **Map** | Leaflet + React-Leaflet |
| **Deployment** | **Vercel** (frontend) + **Railway** (backend) |

---

## 🧠 How It Works

### 1. User inputs
```json
{
  "current_location": "Chicago, IL",
  "pickup_location": "St. Louis, MO",
  "dropoff_location": "Dallas, TX",
  "cycle_used_hours": 0
}
```

### 2. Backend pipeline
1. **Geocode** the 3 locations via Nominatim (cached).
2. **Route** current → pickup and pickup → dropoff via OSRM.
3. **Simulate** the trip against the HOS engine:
   - Drive 11h max per shift.
   - Take a 10-hour reset when limits are hit.
   - Insert 30-min break after 8h of cumulative driving.
   - Refuel every 1,000 miles.
   - Track 70-hour cycle; use 34-hour restart when exceeded.
4. **Match fuel stations** along the route corridor (KD-Tree query).
5. **Return** route geometry + fuel stops + day-by-day logs.

### 3. Frontend
- Renders 4 summary cards.
- Draws the map with two colored legs.
- Lists the cheapest fuel stops.
- Renders one SVG ELD log per simulated day.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) Redis for caching

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py load_fuel_data --limit 100
python manage.py runserver
```

Backend runs on **http://localhost:8000**.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on **http://localhost:5173**.

### Environment Variables

**backend/.env**
```
DEBUG=True
SECRET_KEY=your-secret-key
REDIS_URL=
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**frontend/.env**
```
VITE_API_URL=http://localhost:8000
```

---

## 📡 API Reference

### `GET /api/health/`

```json
{ "status": "ok", "service": "spotter-eld-api" }
```

**Live:** https://spotter-eld-backend-production.up.railway.app/api/health/

### `POST /api/trips/plan/`

**Request:**
```json
{
  "current_location": "Chicago, IL",
  "pickup_location": "St. Louis, MO",
  "dropoff_location": "Dallas, TX",
  "cycle_used_hours": 0
}
```

**Response (abridged):**
```json
{
  "summary": {
    "total_miles": 925.4,
    "total_days": 2,
    "cycle_used_start": 0,
    "cycle_used_end": 13.83
  },
  "route": {
    "leg1": { "type": "LineString", "coordinates": [[-87.6, 41.8], ...] },
    "leg2": { "type": "LineString", "coordinates": [[-90.2, 38.6], ...] }
  },
  "fuel_stations": [
    { "name": "LOVES TRAVEL STOP #173", "city": "Lawrence", "state": "KS", "price": 3.229 }
  ],
  "daily_logs": [
    {
      "date": "2026-10-02T00:00:00",
      "events": [
        { "status": "driving", "start": "...", "end": "...", "hours": 11.0 },
        { "status": "off_duty", "start": "...", "end": "...", "hours": 10.0 }
      ],
      "totals": {
        "off_duty": 10.0, "sleeper": 0.0, "driving": 11.0, "on_duty": 2.5
      }
    }
  ]
}
```

**Live:** https://spotter-eld-backend-production.up.railway.app/api/trips/plan/

---

## 🧮 HOS Rules Engine

The engine (`backend/apps/trips/services/hos_calculator.py`) is a discrete-event simulator implementing:

| Rule | Value | Reference |
|---|---|---|
| Max driving per shift | **11 h** | FMCSA §395.3(a)(3) |
| Max driving window | **14 h** | Includes all on-duty time |
| Break required | **30 min** | After 8 h cumulative driving |
| Daily reset | **10 h** | Off-duty or sleeper |
| Weekly cycle | **70 h / 8 days** | Property-carrying |
| Cycle restart | **34 h** | Optional reset |
| Fuel interval | **1,000 mi** | Assessment assumption |
| Pickup / Dropoff | **1 h each** | On-duty, not driving |

Each event is logged with `status`, `start`, `end`, `location`, and `note`, ready for the frontend to draw.

---

## 📂 Project Structure

```
spotter-eld-trip-planner/
├── backend/
│   ├── config/                     # Django project
│   │   ├── settings/               # base / dev / prod
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── trips/                  # Trip planning + HOS
│   │   │   ├── services/
│   │   │   │   ├── geocoding.py    # Nominatim wrapper
│   │   │   │   ├── routing.py      # OSRM wrapper
│   │   │   │   ├── hos_calculator.py   ⭐ Rules engine
│   │   │   │   └── trip_planner.py     ⭐ Orchestrator
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   └── fuel/                   # Fuel stations + KD-Tree
│   │       ├── models.py
│   │       ├── services/optimization.py
│   │       └── management/commands/load_fuel_data.py
│   ├── data/
│   │   └── fuel-prices-for-be-assessment.csv
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TripForm.jsx
│   │   │   ├── RouteMap.jsx
│   │   │   ├── ELDLogSheet.jsx    ⭐ SVG renderer
│   │   │   ├── TripSummary.jsx
│   │   │   ├── StopsTimeline.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── pages/Home.jsx
│   │   ├── api/client.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── Dockerfile
├── .gitignore
└── README.md
```

---

## 🚀 Deployment

### Backend → Railway

- **Service:** `spotter-eld-backend`
- **Root:** repo root (Dockerfile builds from `backend/`)
- **Builder:** Dockerfile
- **Environment Variables:**
  - `DEBUG=False`
  - `SECRET_KEY=<random>`
  - `ALLOWED_HOSTS=*`
  - `CORS_ALLOWED_ORIGINS=https://spotter-eld-frontend-ten.vercel.app`
  - `DATABASE_URL` (auto-injected by Railway PostgreSQL)
- **Live URL:** https://spotter-eld-backend-production.up.railway.app

### Frontend → Vercel

- **Project:** `spotter-eld-frontend`
- **Root Directory:** `frontend`
- **Framework:** Vite
- **Environment Variables:**
  - `VITE_API_URL=https://spotter-eld-backend-production.up.railway.app`
- **Live URL:** https://spotter-eld-frontend-ten.vercel.app

---

## 🗺️ Roadmap

- [ ] Multi-vehicle support (different ranges, MPG)
- [ ] Adverse driving conditions exception
- [ ] Sleeper berth split provision
- [ ] PDF export of ELD sheets
- [ ] Real-time traffic integration
- [ ] Driver authentication + saved trips

---

## 👨‍💻 Author

**Osama Sadek**

- **GitHub:** [@Eng-Osama-Sadek](https://github.com/Eng-Osama-Sadek)
- **Live Demo:** [spotter-eld-frontend-ten.vercel.app](https://spotter-eld-frontend-ten.vercel.app)
- **Repository:** [spotter-eld-trip-planner](https://github.com/Eng-Osama-Sadek/spotter-eld-trip-planner)

> *"I build full-stack products that solve real-world problems — combining clean architecture, thoughtful UX, and pragmatic automation. This project demonstrates my ability to translate dense federal regulations (FMCSA HOS) into a working, deployable software system with AI-assisted development workflows."*

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [FMCSA](https://www.fmcsa.dot.gov/) — Hours-of-Service regulations source
- [OSRM](http://project-osrm.org/) — Free routing engine
- [Nominatim](https://nominatim.org/) — Free geocoding
- [Leaflet](https://leafletjs.com/) — Open-source map library
- [Vercel](https://vercel.com/) — Frontend hosting
- [Railway](https://railway.app/) — Backend hosting
- [Spotter](https://spotter.ai/) — For the assessment opportunity

---

<p align="center">
  <strong>⭐ Star this repo if you find it useful! ⭐</strong><br>
  Built with ❤️ using Django, React, and AI-assisted development
</p>