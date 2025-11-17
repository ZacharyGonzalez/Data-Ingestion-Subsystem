import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def read_csv(PATH) -> pd.DataFrame:
    logger.info(f'Reading healthcare data from {PATH}.')
    p = Path(PATH)
    if not p.exists():
        raise FileNotFoundError(PATH)
    df = pd.read_csv(p)
    logger.info(f'Successfully read healthcare data from {PATH}.')
    return df