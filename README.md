# Sales Forecast Data Pipeline

End-to-end Data Science project: **ETL → PostgreSQL → ML → API → Dashboard → Telegram monitoring**.

🔗 **GitHub:** https://github.com/Sailauov08/Mega_project

---

## What it does

```
CSV data
   ↓
ETL (load, clean, validate, daily metrics)
   ↓
PostgreSQL database
   ↓
ML model (RandomForest sales forecast)
   ↓
FastAPI REST API
   ↓
Streamlit dashboard
   ↓
Telegram bot (nightly alerts at 03:00)
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| Database | PostgreSQL |
| ETL | Pandas, SQLAlchemy |
| ML | Scikit-learn, Joblib |
| API | FastAPI, Uvicorn |
| Dashboard | Streamlit, Plotly |
| Monitoring | Telegram Bot API |
| Automation | Windows Task Scheduler |

---

## Project Structure

```
Mega_project/
├── config/          # Settings (.env)
├── db/              # Schema, connection, init
├── etl/             # ETL pipeline
├── ml/              # Train, predict, evaluate
├── api/             # FastAPI endpoints
├── dashboard/       # Streamlit app
├── bot/             # Telegram notifier
├── scripts/         # Sample data, nightly pipeline
├── data/raw/        # CSV input
└── models/          # Trained model (local)
```

---

## Quick Start (Local)

### 1. Clone & install

```bash
git clone https://github.com/Sailauov08/Mega_project.git
cd Mega_project
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure `.env`

Copy `.env.example` → `.env` and fill in:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sales_db
DB_USER=postgres
DB_PASSWORD=your_password

TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. PostgreSQL

Create database:

```sql
CREATE DATABASE sales_db;
```

### 4. Run pipeline

```bash
python scripts/generate_sample_data.py
python db/init_db.py
python etl/run_etl.py
python ml/run_ml.py
```

### 5. Start services

```bash
# API
uvicorn api.main:app --reload
# → http://127.0.0.1:8000/docs

# Dashboard
streamlit run dashboard/app.py
# → http://localhost:8501

# Telegram test
python bot/test_telegram.py

# Nightly pipeline (manual)
python scripts/nightly_pipeline.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server, DB, model status |
| GET | `/metrics` | MAE, RMSE |
| GET | `/latest-data` | Recent daily metrics |
| GET | `/predictions` | Model predictions |
| POST | `/predict` | Predict sales from features |
| GET | `/predict/latest` | Predict from latest day |
| GET | `/docs` | Swagger UI |

---

## Docker (optional)

```bash
docker-compose up --build
```

API: http://localhost:8000/docs

---

## Deploy to Render (free tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect repo `Sailauov08/Mega_project`
4. Settings:
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
5. Add **PostgreSQL** database on Render
6. Set environment variables: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
7. After deploy, run init via Render shell:
   ```bash
   python db/init_db.py
   python scripts/generate_sample_data.py
   python etl/run_etl.py
   python ml/run_ml.py
   ```

Live API: `https://your-app.onrender.com/health`

---

## Streamlit Cloud (dashboard)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repo
3. Main file: `dashboard/app.py`
4. Add secrets (DB credentials) in Streamlit settings

---

## Nightly Automation (Windows)

Task Scheduler runs daily at **03:00**:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register_scheduled_task.ps1
```

Or run manually:

```bash
python scripts/nightly_pipeline.py
```

---

## Resume Keywords

Python · Pandas · SQL · PostgreSQL · ETL · Data Cleaning · Scikit-learn · FastAPI · Streamlit · Docker · Telegram Bot · Task Scheduler · ML Deployment

---

## Author

**Bekarys** — Data Science Portfolio Project
