from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv
import psycopg2
import os
import logging
import time
from logger import log_function_call

logger = logging.getLogger(__name__)

load_dotenv()
DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
pool = None

@log_function_call
def init_pool(retries=5, delay=3):
    global pool
    if pool is not None:
        logger.info("Using already existing pool")
        return pool
    for i in range(retries):
        try:
            logger.info("Trying to initialize connection (%s/%s)", i + 1, retries)
            pool = SimpleConnectionPool(
                minconn=1,
                maxconn=1,
                database=DATABASE,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
            )
            return pool
        except Exception as e:  # TODO make the exception handler more specific
            logger.exception("Pool init failed: %s", e)
            time.sleep(delay)
    raise RuntimeError("Could not initialize postgress pool after retries.")


@contextmanager
def get_connection():
    pool=init_pool()
    conn = pool.getconn()
    try:
        yield conn
    except Exception as e:
        logger.error("Error while getting or using a pooled connection: %s", e)
        raise
    finally:
        if conn:
            pool.putconn(conn)
