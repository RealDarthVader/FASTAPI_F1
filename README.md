# 🏎️ FastF1 Live Dashboard

A full-stack Formula 1 dashboard built with **FastAPI, FastF1, SQLite, SQLAlchemy, and React (Vite)**. The project combines F1 race data and telemetry with a web-based dashboard, backed by a REST API and deployed on Render.

## 🌐 Live Demo

| Service | Link |
|---|---|
| 🚀 **Frontend** | https://fastapi-f1-frontend.onrender.com/ |
| ⚙️ **Backend API** | https://fastapi-f1-lz8j.onrender.com/ |
| 📚 **API Docs** | https://fastapi-f1-lz8j.onrender.com/docs |
| 💻 **GitHub** | https://github.com/RealDarthVader/FASTAPI_F1 |

## ✨ Features

- 🗓️ **Race Calendar** — View F1 season schedules and Grand Prix information.
- 🏁 **Grand Prix Results** — Retrieve race results, podiums, and driver data using FastF1.
- 📊 **F1 Telemetry** — Access Formula 1 session and telemetry data through FastF1.
- ⭐ **Driver Favorites** — Save and manage favorite drivers using SQLite persistence.
- ⚡ **Caching** — Cache expensive FastF1 data requests to reduce repeated downloads and improve response times.
- 🔌 **REST API** — FastAPI backend with automatically generated Swagger/OpenAPI documentation.
- 🖥️ **React Dashboard** — Vite-powered frontend for interacting with the API and viewing F1 data.
- ☁️ **Cloud Deployment** — Frontend and backend deployed as separate Render services.

## 🛠️ Tech Stack

### Backend

- **Python**
- **FastAPI**
- **FastF1**
- **SQLAlchemy**
- **SQLite**
- **Uvicorn**

### Frontend

- **React**
- **Vite**
- **JavaScript**
- **CSS**

### Deployment

- **Render** — Frontend Static Site + Backend Web Service

## 📁 Project Structure

```text
FASTAPI_F1/
│
├── Backend/
│   ├── app/
│   │   ├── database.py       # Database connection and session handling
│   │   ├── main.py           # FastAPI application and CORS configuration
│   │   ├── models.py         # SQLAlchemy database models
│   │   └── routers/          # API route handlers
│   │
│   ├── Dockefile             # Backend container configuration
│   └── requirements.txt      # Python dependencies
│
├── Frontend/
│   ├── src/                  # React application source
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies and scripts
│   ├── vite.config.js        # Vite configuration
│   └── vercel.json           # Frontend deployment configuration
│
├── api/                      # API/deployment-related files
├── requirements.txt          # Project-level Python dependencies
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/RealDarthVader/FASTAPI_F1.git
cd FASTAPI_F1
```

### 2. Start the Backend

```bash
cd Backend
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

### 3. Start the Frontend

Open a new terminal:

```bash
cd Frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/races/{year}` | Get the race calendar for a season |
| `GET` | `/drivers/{year}/{gp}` | Get race results for a Grand Prix |
| `GET` | `/favorites` | Get saved favorite drivers |
| `POST` | `/favorites` | Add a driver to favorites |
| `DELETE` | `/favorites/{driver_code}` | Remove a favorite driver |
| `GET` | `/docs` | Interactive Swagger API documentation |

### Example Requests

Get the 2026 F1 calendar:

```http
GET /races/2026
```

Get race results:

```http
GET /drivers/2026/Belgian
```

## ⚡ FastF1 & Caching

FastF1 provides access to Formula 1 timing, session, telemetry, and race data. Some FastF1 operations can require significant data loading, so the backend uses caching to avoid repeatedly downloading the same information.

This makes repeated API requests more efficient during dashboard usage and development.

## 🗄️ Data Persistence

The application uses **SQLite** with **SQLAlchemy** for local persistence.

The database layer handles database connections and sessions, while SQLAlchemy models define persistent entities such as favorite drivers.

## ☁️ Deployment

The application is deployed as two services on Render:

```text
                         ┌──────────────────────────┐
                         │       React + Vite       │
                         │        Frontend          │
                         └────────────┬─────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌──────────────────────────┐
                         │         FastAPI          │
                         │         Backend          │
                         └──────────┬───────┬───────┘
                                    │       │
                             ┌──────┘       └──────┐
                             ▼                     ▼
                     ┌──────────────┐      ┌──────────────┐
                     │    FastF1    │      │    SQLite    │
                     │  F1 Dataset  │      │  Persistence │
                     └──────────────┘      └──────────────┘
```

### Production Services

**Frontend**

https://fastapi-f1-frontend.onrender.com/

**Backend**

https://fastapi-f1-lz8j.onrender.com/

**Swagger API Docs**

https://fastapi-f1-lz8j.onrender.com/docs

## 🔮 Future Improvements

- Live race timing and telemetry updates
- Driver-vs-driver comparison
- Lap-time and sector analysis
- Circuit maps and track visualization
- Tire strategy visualization
- Pit-stop analysis
- Championship points graphs
- WebSocket-based live updates
- User authentication
- PostgreSQL for production-scale persistence
- More advanced telemetry charts and analytics

## 📄 License

This project is open-source. A license file can be added to the repository if you intend to distribute the project formally.

---

