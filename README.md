# Data Ingestion SubSystem

This project aims to implement an ETL pipeline, from csv to relational database, and then present actionable/interesting results.

## How to setup

Simply go to the root directory, fill out the .env with your postgres db and pgadmin info (check dotenv_template for format) and then run:
    ```docker compose up --build```


## Drop Duplicates or NA

By checking for collisions on insert of a row, we can detect duplicate entries and avoid costly transactions.
Per chunk checking for duplicates also removes the occasional duplicate as well.

Per chunk checking for NA entries if efficient enough for our use case.

## The dataset

Sparks could be used but seeing as to how the CSV fits into memory comfortably, we only chunk it with pandas for practice working with partitioned data.

Docker is used to host the postgres server, with psycopg2 acting as the driver to connect with it.

Docker also hosts pgadmin4 which when connected to the database allows for monitoring and querying of the data.