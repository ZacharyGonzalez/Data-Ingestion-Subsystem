import pandas as pd
from pathlib import Path

def get_csv(path:str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(p)