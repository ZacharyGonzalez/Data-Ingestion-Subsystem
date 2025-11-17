import pandas as pd
from pathlib import Path

def get_csv(path:str, logger) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(p)

    
def read_csv(logger, PATH):
    logger.info(f'Reading healthcare data from {PATH}.')
    df = get_csv(PATH, logger)
    return df