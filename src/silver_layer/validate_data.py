"""Ensure the dataframe adheres to the schema before insertion of data"""

import logging
from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError, StringConstraints, Field
from typing import List, Tuple, Annotated
import pandas as pd
import json

logger = logging.getLogger(__name__)


class RawCSV(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            min_length=4, max_length=40, pattern=r"^[A-Za-z \.]{1,40}$"
        ),  # generic capture for mr. preffix and jr.
    ]
    age: Annotated[int, Field(ge=1, le=100)]
    gender: Annotated[
        str, StringConstraints(min_length=4, max_length=6, pattern=r"^[A-Z][a-z]{3,5}$")
    ]
    blood_type: Annotated[
        str,
        StringConstraints(pattern=r"[A][+-]|[B][+-]|[AB][+-]|[O][+-]"),
    ]
    medical_condition: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z ]{2,40}$"),
    ]
    date_of_admission: datetime
    doctor: Annotated[
        str,
        StringConstraints(
            min_length=4, max_length=40, pattern=r"^[A-Za-z \.]{2,40}$"
        ),  # i am not going to concern myself with mr.,mrs., and jr.'s since regex is not a criterion
    ]
    hospital: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z\-, ]{1,40}$"),
    ]
    insurance_provider: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z\-, ]{1,40}$"),
    ]
    billing_amount: float
    room_number: PositiveInt
    admission_type: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z]{1,40}$"),
    ]
    discharge_date: datetime
    medication: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z]{1,40}$"),
    ]
    test_results: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z]{1,40}$"),
    ]

    def validate_name_proper(name: str) -> bool:
        if len(name.split()) != 2 or len(name) > 40 or len(name) < 3:
            return False
        return True


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
    logger.info("Successfully validated %s rows.", len(valid_rows))
    logger.info("Rejected %s rows.", len(rejects))
    if rejects:
        logger.debug(
            "REJECTS:\n%s", json.dumps(rejects, indent=2)
        )  # TODO maybe log somewhere else?

    return (pd.DataFrame(valid_rows), pd.DataFrame(rejects))
