import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_SCHEMA = """
patients(patient_id, name, age, gender, city, phone, blood_group)
doctors(doctor_id, name, specialization, hospital_name)
appointments(appointment_id, patient_id, doctor_id, appointment_date, status)
diagnosis(diagnosis_id, patient_id, disease, diagnosis_date, severity)
billing(bill_id, patient_id, amount, payment_status, bill_date)

Relationships:
appointments.patient_id = patients.patient_id
appointments.doctor_id = doctors.doctor_id
diagnosis.patient_id = patients.patient_id
billing.patient_id = patients.patient_id
"""


def clean_sql(sql_query: str) -> str:
    return sql_query.replace("```sql", "").replace("```", "").strip()


def fallback_sql_generator(question: str) -> str:
    """Works without API key for local demo. OpenAI will be used when key is provided."""
    q = question.lower()

    if ("diabetic" in q or "diabetes" in q) and "pune" in q and ("50" in q or "above" in q):
        return """
        SELECT p.patient_id, p.name, p.age, p.gender, p.city, p.blood_group, d.disease, d.severity
        FROM patients p
        JOIN diagnosis d ON p.patient_id = d.patient_id
        WHERE d.disease ILIKE 'Diabetes'
          AND p.age > 50
          AND p.city ILIKE 'Pune'
        LIMIT 100;
        """

    if "diabetic" in q or "diabetes" in q:
        return """
        SELECT p.patient_id, p.name, p.age, p.gender, p.city, p.blood_group, d.disease, d.severity
        FROM patients p
        JOIN diagnosis d ON p.patient_id = d.patient_id
        WHERE d.disease ILIKE 'Diabetes'
        LIMIT 100;
        """

    if "unpaid" in q and "bill" in q and ("5000" in q or "5,000" in q):
        return """
        SELECT b.bill_id, p.name, p.city, b.amount, b.payment_status, b.bill_date
        FROM billing b
        JOIN patients p ON b.patient_id = p.patient_id
        WHERE b.payment_status ILIKE 'UNPAID'
          AND b.amount > 5000
        LIMIT 100;
        """

    if "unpaid" in q and "bill" in q:
        return """
        SELECT b.bill_id, p.name, p.city, b.amount, b.payment_status, b.bill_date
        FROM billing b
        JOIN patients p ON b.patient_id = p.patient_id
        WHERE b.payment_status ILIKE 'UNPAID'
        LIMIT 100;
        """

    if "appointment" in q and "today" in q:
        return """
        SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name,
               d.specialization, a.appointment_date, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE a.appointment_date = CURRENT_DATE
        LIMIT 100;
        """

    if "pune" in q:
        return "SELECT patient_id, name, age, gender, city, blood_group FROM patients WHERE city ILIKE 'Pune' LIMIT 100;"

    if "nagpur" in q:
        return "SELECT patient_id, name, age, gender, city, blood_group FROM patients WHERE city ILIKE 'Nagpur' LIMIT 100;"

    if "patient" in q or "patients" in q:
        return "SELECT patient_id, name, age, gender, city, blood_group FROM patients LIMIT 100;"

    return "SELECT patient_id, name, age, gender, city, blood_group FROM patients LIMIT 10;"


def generate_sql_from_question(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key or api_key == "your_openai_api_key_here":
        return clean_sql(fallback_sql_generator(question))

    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an expert PostgreSQL SQL generator for a healthcare database.

Convert the user message into ONE safe PostgreSQL SELECT query.

Rules:
- Return only SQL query.
- Only SELECT queries are allowed.
- Do not return explanation.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, COPY.
- Use only tables and columns from the schema.
- Use JOIN when required.
- Use ILIKE for text search where useful.
- Limit result to 100 rows unless user asks for count or aggregation.
- Do not expose phone number unless user specifically asks for phone.

Schema:
{DATABASE_SCHEMA}

User message:
{question}
"""

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
    )

    return clean_sql(response.output_text)
