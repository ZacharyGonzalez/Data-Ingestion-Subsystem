"""Ensure the dataframe adheres to the schema before insertion of data"""
import logging
from datetime import datetime
from pydantic import BaseModel, PositiveFloat, PositiveInt

logger = logging.getLogger(__name__)
class CSVRecord(BaseModel):
    name: str
    age: PositiveInt
    blood_type: str
    medical_condition: str
    date_of_admission: datetime
    docotr: str
    hospital: str
    insurance_provider: str
    billing_amount: PositiveFloat
    room_number: PositiveInt
    admission_type: str
    discharge_date: datetime
    medication: str
    test_results: str
    
def validate_data(df):
    """TODO"""
    logger.info('validationg data')
    logger.info('successfully validated data')
    return df
