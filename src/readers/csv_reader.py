"""General safe handler for CSV Reading"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def safe_read_csv(path) -> pd.DataFrame:
    """Safe checker for CSV Reading"""
    logger.info("Reading data from %s.", path)
    try:
        df = pd.read_csv(path)
        logger.info("Successfully read data from %s.", path)
    except:
        logger.exception('Failed to read from %s, does it exist?',path)
        raise
    return df
