DROP TABLE IF EXISTS RAWCSV;
DROP TABLE IF EXISTS CSVRejects;
DROP TABLE IF EXISTS Patient;
DROP TABLE IF EXISTS Admissions;
DROP TABLE IF EXISTS Insurance;
DROP TABLE IF EXISTS Medical_Record;

CREATE TABLE IF NOT EXISTS RawCSV (
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
CREATE TABLE IF NOT EXISTS CSVRejects (
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

CREATE TABLE IF NOT EXISTS Patient(
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age SMALLINT,
    gender VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Medical_Record(
    patient_id INT REFERENCES Patient(patient_id) ON DELETE CASCADE,
    blood_type VARCHAR(5),
    medical_condition VARCHAR(100),
    medication VARCHAR(100),
    test_results VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Insurance(
    insurance_claim SERIAL PRIMARY KEY,
    insurance_provider VARCHAR(50),
    billing_amount NUMERIC(10,2),
    patient_id INT REFERENCES Patient(patient_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  Admissions(
    admission_id SERIAL PRIMARY KEY,
    hospital VARCHAR(50),
    room_number SMALLINT,
    date_of_admission DATE,
    discharge_date DATE,
    admission_type VARCHAR(20),
    patient_id INT REFERENCES Patient(patient_id) ON DELETE CASCADE
);