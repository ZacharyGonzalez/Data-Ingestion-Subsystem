"""Ensure the dataframe adheres to the schema before insertion of data"""

import logging
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError
from typing import List, Tuple
import pandas as pd
import json

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
            rejects.append({"idx": i, "row": row.to_dict(), "error": e.errors()})
    logger.info("Successfully validated %s rows", len(valid_rows))
    logger.info("Rejected %s rows", len(rejects))
    if rejects:
        logger.info("REJECTS:\n%s", json.dumps(rejects, indent=2))

    return (pd.DataFrame(valid_rows), rejects)
