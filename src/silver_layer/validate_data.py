"""Ensure the dataframe adheres to the schema before insertion of data"""

import logging
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError
from typing import List, Tuple
import pandas as pd

logger = logging.getLogger(__name__)


class RawCSV(BaseModel):
    name: str
    age: PositiveInt
    gender: str
    blood_type: str
    medical_condition: str
    date_of_admission: datetime
    doctor: str
    hospital: str
    insurance_provider: str
    billing_amount: float
    room_number: PositiveInt
    admission_type: str
    discharge_date: datetime
    medication: str
    test_results: str


class Admissions(BaseModel):
    admission_id: PositiveInt  # Surrogate PK
    hospital: str
    room_number: PositiveInt
    date_of_admission: datetime
    discharge_date: datetime
    admission_type: str
    patient_id: PositiveInt  # FK


class Insurance(BaseModel):
    insurance_claim: PositiveInt  # Surrogate PK
    insurance_provider: str
    billing_amount: int
    patient_id: PositiveInt  # FK


class Patient(BaseModel):
    patient_id: PositiveInt  # Surrogate PK
    name: str
    age: PositiveInt
    gender: str
    blood_type: str
    medical_condition: str
    medication: str
    test_results: str


def validate_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[dict]]:
    """Compares Dataframe to RawCSV pydantic class
    returns a tuple containing a dataframe and a list of dict rejects
    """
    valid_rows = []
    rejects = []
    logger.info("Validating data...")

    for i, row in df.iterrows():
        try:
            valid_row = RawCSV(**row.to_dict())
            valid_rows.append(valid_row.model_dump())
        except ValidationError as e:
            rejects.append((i, row.to_dict(), e.errors()))  # this is absurdly long

    logger.info("Successfully validated %s rows", len(valid_rows))
    logger.info("Rejected %s rows", len(rejects))
    return (pd.DataFrame(valid_rows), rejects)
