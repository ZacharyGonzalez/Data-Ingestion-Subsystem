import logging
import pandas as pd

logger = logging.getLogger(__name__)

def safe_read_csv(path: str, chunk_size: int):
    """Safe CSV reader that yields chunks."""
    logger.info("Reading data from %s.", path)
    try:
        reader = pd.read_csv(path, chunksize=chunk_size)
        logger.info("Successfully opened %s for chunked reading.", path)
        for i, chunk in enumerate(reader, start=1):
            logger.info("Yielding chunk %s with %s rows.", i, len(chunk))
            logger.info('\n%s',chunk)
            yield chunk
    except Exception as e:
        logger.exception('Failed to read %s: %s', path, e)
        raise
