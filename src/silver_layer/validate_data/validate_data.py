"""Ensure the dataframe adheres to the schema before insertion of data"""

import logging
import json
from typing import List, Tuple
from pydantic import ValidationError
import pandas as pd
from logger import log_function_call
from .validators.raw_csv import RawCSV

logger = logging.getLogger(__name__)


@log_function_call
def validate_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[dict]]:
    """Compares Dataframe to custom RawCSV pydantic class
    returns a tuple containing a dataframe and a list of dict rejects
    """
    valid_rows = []
    rejects = []

    for i, row in df.iterrows():
        try:
            valid_row = RawCSV(**row.to_dict())
            valid_rows.append(valid_row.model_dump())
        except ValidationError as e:
            rejects.append({"idx": i, "row": row.to_dict(), "error": e.errors()})
    logger.info(
        "--Successfully validated %s rows and rejected %s rows.",
        len(valid_rows),
        len(rejects),
    )
    if rejects:
        for reject in rejects:
            rejected_row = (
                reject["row"],
                reject["error"][0]["loc"],
                reject["error"][0]["msg"],
            )
            logger.warning(
                "rejected rows: %s",
                rejected_row,
            )

    return (pd.DataFrame(valid_rows), pd.DataFrame(rejects))
