"""General safe handler for CSV Reading"""

import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


def read_csv(path) -> pd.DataFrame:
    """Safe checker for CSV Reading"""
    logger.info("Reading healthcare data from %s.", path)
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(p)
    logger.info("Successfully read healthcare data from %s.", path)
    return df
