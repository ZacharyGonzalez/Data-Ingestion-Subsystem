# Data Ingestion SubSystem

A containerized ETL platform engineered to ingest raw healthcare CSVs, validate and clean the data, and load it into a fully normalized PostgreSQL database.  
The workflow aligns with the **Medallion Architecture (Bronze → Silver → Gold)**:

- **Bronze:** Raw CSV ingestion (chunked to simulate large-scale datasets).  
- **Silver:** Data cleaning, deduplication, and Pydantic-based validation.  
- **Gold:** Normalized tables loaded via `psycopg2` connection pooling.

All components run inside Docker, ensuring an isolated, reproducible, and environment-agnostic deployment.  
The final state provides a structured operational datastore ready for **Power BI analytics and reporting**.


## How to setup

1. Navigate to the project root directory.
2. Fill out the `.env` file with Postgres and pgAdmin credentials (use `dotenv_template` as a reference).  
3. Start the environment by running:

    ```docker compose up --build```

To access pgadmin4, go to localhost:5050, login with details added to the .env and follow the steps below.

## Accessing pgAdmin4

Open your browser and go to:
[http://localhost:5050](http://localhost:5050)

Log in with the credentials from your .env, then:

### Step 1: Register a New Server

Left sidebar → Servers (right-click) → Register → Server

### Step 2: General tab

- **Name:** `source_postgres`

### Step 3: Connection tab

- **Host:** `source_postgres`  
    (use the _container name_, not localhost)
- **Port:** `5432`
- **Username:** `postgres`
- **Password:** `secret`
- Save password: **✔**

## How This project works

- PostgreSQL runs inside Docker as the primary data store.
- The ETL application connects via psycopg2 using connection pools for efficient batch inserts.
- pgAdmin4 provides dashboarding, SQL execution, and ERD visualization.
- This architecture delivers:
  - A deterministic environment
  - Clean separation of services
  - Simplified onboarding and operational consistency


## To run the tests
- Run `pip install -e .`
- Then run `pytest` in the cli