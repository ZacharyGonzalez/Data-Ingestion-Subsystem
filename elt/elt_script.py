import os
import subprocess
import time
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='./logs/etl_pipeline.log',
    filemode='w',
    encoding='utf-8',
    level=logging.INFO)
logger.info('Logger Initialization success.')


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host],
                check=True,
                capture_output=True,
                text=True,
            )
            if "accepting connections" in result.stdout:
                print(f"{host} is accepting connections.")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to {host}: {e}")
        retries += 1
        print(f"Retrying in {delay_seconds}s (attempt {retries}/{max_retries})")
        time.sleep(delay_seconds)

    print(f"Max retries reached for {host}.")
    return False


# Wait for both databases
if not wait_for_postgres(host="source_postgres"):
    raise SystemExit("Source Postgres not ready, exiting.")

if not wait_for_postgres(host="destination_postgres"):
    raise SystemExit("Destination Postgres not ready, exiting.")

print("Starting ELT script...")

source_config = {
    "dbname": "source_db",
    "user": "postgres",
    "password": "secret",
    "host": "source_postgres",
}

destination_config = {
    "dbname": "destination_db",
    "user": "postgres",
    "password": "secret",
    "host": "destination_postgres",
}

# Environment with PATH preserved
env_dump = {**os.environ, "PGPASSWORD": source_config["password"]}

dump_command = [
    "pg_dump",
    "-h",
    source_config["host"],
    "-U",
    source_config["user"],
    "-d",
    source_config["dbname"],
    "-f",
    "data_dump.sql",
    "-w",
]

print("Running pg_dump from source...")
subprocess.run(dump_command, env=env_dump, check=True)
print("Dump completed.")

env_load = {**os.environ, "PGPASSWORD": destination_config["password"]}

load_command = [
    "psql",
    "-h",
    destination_config["host"],
    "-U",
    destination_config["user"],
    "-d",
    destination_config["dbname"],
    "-a",
    "-f",
    "data_dump.sql",
]

print("Running psql to load into destination...")
subprocess.run(load_command, env=env_load, check=True)
print("Load completed.")

print("Ending ELT script.")
