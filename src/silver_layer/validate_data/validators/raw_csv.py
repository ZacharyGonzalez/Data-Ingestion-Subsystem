from typing import Annotated
from datetime import datetime
from pydantic import BaseModel, PositiveInt, StringConstraints, Field


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
        StringConstraints(pattern=r"^[A][+-]|^[B][+-]|^[A][B][+-]|^[O][+-]"),
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
        ),  # i am not going to concern myself with mr.,mrs., and jr.'s names
    ]
    hospital: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z\-, ]{1,40}$"),
    ]
    insurance_provider: Annotated[
        str,
        StringConstraints(min_length=3, max_length=40, pattern=r"^[A-Za-z\-, ]{1,40}$"),
    ]
    billing_amount: float  # Can have negative bills
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
