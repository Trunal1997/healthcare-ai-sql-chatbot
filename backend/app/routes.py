from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ChatRequest
from app.sql_generator import generate_sql_from_question
from app.sql_validator import validate_sql

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "running", "message": "Healthcare AI SQL Chatbot API is working"}


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    sql_query = generate_sql_from_question(request.message)

    if not validate_sql(sql_query):
        raise HTTPException(status_code=400, detail="Unsafe SQL query blocked. Only SELECT queries are allowed.")

    try:
        result = db.execute(text(sql_query))
        rows = [dict(row) for row in result.mappings().all()]

        if rows:
            assistant_message = f"I found {len(rows)} record(s) matching your question."
        else:
            assistant_message = "I could not find matching records for your question."

        return {
            "user_message": request.message,
            "assistant_message": assistant_message,
            "sql_query": sql_query.strip(),
            "data": rows,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(exc)}")
