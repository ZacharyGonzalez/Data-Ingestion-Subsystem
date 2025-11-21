DROP TABLE IF EXISTS rawcsv;
DROP TABLE IF EXISTS csvrejects;
DROP TABLE IF EXISTS visit;
DROP TABLE IF EXISTS claim;
DROP TABLE IF EXISTS diagnosis;
DROP TABLE IF EXISTS patient;

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

CREATE TABLE IF NOT EXISTS patient(
    patient_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age SMALLINT,
    gender VARCHAR(10),
    blood_type VARCHAR(5),
    UNIQUE (name,age,gender,blood_type)
);


CREATE TABLE IF NOT EXISTS diagnosis(
    diagnosis_id SERIAL PRIMARY KEY,
	patient_id INTEGER REFERENCES patient(patient_id) ON DELETE CASCADE,
	doctor VARCHAR(50),
	medical_condition VARCHAR(100),
	medication VARCHAR(100),
	test_results VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS visit(
	visit_id SERIAL PRIMARY KEY,
	patient_id INTEGER REFERENCES patient(patient_id) ON DELETE CASCADE,
    diagnosis_id INTEGER REFERENCES diagnosis(diagnosis_id), /*not cascading this because a visit and patient still exist*/
	hospital VARCHAR(50),
	room_number SMALLINT,
	date_of_admission DATE,
	discharge_date DATE,
	admission_type VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS claim(
    claim_id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patient(patient_id) ON DELETE CASCADE,
    insurance_provider VARCHAR(50),
	billing_amount NUMERIC(10,2)
);