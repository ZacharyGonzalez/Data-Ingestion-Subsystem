# Data Ingestion SubSystem

This project aims to implement an ETL pipeline, from csv to relational database, and then present actionable/interesting results.

## How to setup

Go to the root directory, fill out the .env with your postgres db and pgadmin info (check dotenv_template for format, the pgadmin info will be used to set the new connection to the DB) and then run:
    ```docker compose up --build```

To access pgadmin4, go to localhost:5050, login with details added to the .env and follow the steps below.

**Step 1: Add new server**

Left sidebar → **Servers (right-click)** → **Register → Server**

**Step 2: General tab**
- **Name:** `source_postgres`
    
**Step 3: Connection tab**

Fill in:
- **Host:** `source_postgres`  
    (use the _container name_, not localhost)

- **Port:** `5432`

- **Username:** `postgres`
    
- **Password:** `secret`
    
- Save password: **✔**
  
  
## How This project works

Docker is used to host the postgres server, with psycopg2 acting as the driver to connect with it.

Docker also hosts pgadmin4 which when connected to the database allows for monitoring and querying of the data and can show the ERD.

## Drop Duplicates or NA

By checking for collisions on insert of a row, we can detect duplicate entries and avoid costly transactions.

Per chunk checking for duplicates also removes the occasional duplicate as well.

The entire dataset is chunked and then validated by Pydantic before moving through to cleaning.

## The dataset

Sparks could be used but seeing as to how the CSV fits into memory comfortably, we only chunk it with pandas for practice working with partitioned data.