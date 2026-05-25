# Healthcare AI SQL Chatbot

An AI-powered chatbot that converts healthcare questions in plain English into safe PostgreSQL `SELECT` queries and displays results in a professional chat UI.

## Features

- Chatbot-style React UI
- FastAPI backend
- PostgreSQL healthcare database
- Text-to-SQL generation
- OpenAI integration when API key is available
- Local fallback rules for demo without API key
- SQL safety validator: only `SELECT` queries are allowed
- Healthcare tables: patients, doctors, appointments, diagnosis, billing

## Project Structure

```text
healthcare-ai-sql-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   ├── sql_generator.py
│   │   └── sql_validator.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   └── package.json
├── database/
│   ├── schema.sql
│   └── sample_data.sql
└── README.md
```

## 1. Create PostgreSQL Database

Create database:

```sql
CREATE DATABASE healthcare_sql_db;
```

Run these files inside the `database` folder:

```bash
psql -U postgres -d healthcare_sql_db -f schema.sql
psql -U postgres -d healthcare_sql_db -f sample_data.sql
```

Or use pgAdmin Query Tool and run `schema.sql` first, then `sample_data.sql`.

## 2. Backend Setup

```bash
cd backend
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example`:

```env
DATABASE_URL=postgresql://postgres:root@localhost:5432/healthcare_sql_db
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

If you do not add an OpenAI key, the project still runs using local fallback demo rules.

Run backend:

```bash
uvicorn app.main:app --reload
```

Swagger URL:

```text
http://127.0.0.1:8000/docs
```

## 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Sample Questions

```text
Show diabetic patients above age 50 from Pune
Show unpaid bills above 5000
Show today appointments
Show all patients from Nagpur
```

## Interview Explanation

This project is an AI-powered healthcare analytics chatbot. Non-technical healthcare users can ask questions in simple English. The backend uses an LLM to generate a safe SQL query, validates that only `SELECT` queries are allowed, executes the query on PostgreSQL, and returns the result in a conversational UI.

## Safety Design

The app blocks dangerous SQL operations like:

```sql
INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE
```

Only `SELECT` queries are executed.
