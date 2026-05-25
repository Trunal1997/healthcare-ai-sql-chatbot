DROP TABLE IF EXISTS billing;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20),
    city VARCHAR(50),
    phone VARCHAR(20),
    blood_group VARCHAR(10)
);

CREATE TABLE doctors (
    doctor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    hospital_name VARCHAR(100)
);

CREATE TABLE appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    doctor_id INT REFERENCES doctors(doctor_id),
    appointment_date DATE,
    status VARCHAR(30)
);

CREATE TABLE diagnosis (
    diagnosis_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    disease VARCHAR(100),
    diagnosis_date DATE,
    severity VARCHAR(30)
);

CREATE TABLE billing (
    bill_id SERIAL PRIMARY KEY,
    patient_id INT REFERENCES patients(patient_id),
    amount DECIMAL(10,2),
    payment_status VARCHAR(30),
    bill_date DATE
);
