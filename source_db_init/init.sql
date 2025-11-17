DROP TABLE IF EXISTS healthcare;

CREATE TABLE IF NOT EXISTS healthcare (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age SMALLINT,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100),
    date_of_admission DATE,
    doctor VARCHAR(50),
    hospital VARCHAR(50),
    insurance_provider VARCHAR(50),
    billing_amount NUMERIC(10,2),
    room_number SMALLINT,
    admission_type VARCHAR(20),
    discharge_date DATE,
    medication VARCHAR(100),
    test_results VARCHAR(50)
);
