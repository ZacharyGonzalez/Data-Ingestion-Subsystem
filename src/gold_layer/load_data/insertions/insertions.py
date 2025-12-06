DIAGNOSIS_INSERT = """
    INSERT INTO diagnosis(patient_id,  doctor,  medical_condition, medication, test_results)
    values (%s, %s, %s, %s, %s)
    """
PATIENT_INSERT = """
    INSERT INTO patient(name, age, gender, blood_type, date_of_admission, discharge_date, admission_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (name,age,gender,blood_type,date_of_admission,admission_type)
    DO UPDATE SET discharge_date = EXCLUDED.discharge_date
    RETURNING patient_id, (xmax = 0) AS inserted;
    """
CLAIM_INSERT = """
    INSERT INTO claim(patient_id, insurance_provider, billing_amount)
    VALUES (%s, %s, %s)
    """
LOCATION_INSERT = """
    INSERT INTO visit(patient_id, hospital, room_number)
    VALUES (%s, %s, %s)
    """


def patient_insertion(curr, row):
    curr.execute(
        PATIENT_INSERT,
        (
            row["name"],
            row["age"],
            row["gender"],
            row["blood_type"],
            row["date_of_admission"],
            row["discharge_date"],
            row["admission_type"],
        ),
    )
    patient_id, inserted = curr.fetchone()
    return patient_id, inserted


def claim_insertion(curr, row, patient_id):
    curr.execute(
        CLAIM_INSERT,
        (patient_id, row["insurance_provider"], row["billing_amount"]),
    )


def diagnosis_insertion(curr, row, patient_id):
    curr.execute(
        DIAGNOSIS_INSERT,
        (
            patient_id,
            row["doctor"],
            row["medical_condition"],
            row["medication"],
            row["test_results"],
        ),
    )


def location_insertion(
    curr,
    row,
    patient_id,
):
    curr.execute(
        LOCATION_INSERT,
        (
            patient_id,
            row["hospital"],
            row["room_number"],
        ),
    )
