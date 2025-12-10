"""
These queries are here for genneral queries to show i can access and get some kind of info from the DB
"""


import pandas as pd
from db_connection.db_pool import get_connection

def top_conditions(limit=10):
    sql = """
        SELECT medical_condition, COUNT(*) AS occurrences
        FROM diagnosis
        GROUP BY medical_condition
        ORDER BY occurrences DESC
        LIMIT %s;
    """
    with get_connection() as conn:
        return pd.read_sql(sql, conn, params=[limit])

def avg_billing_by_insurance():
    sql = """
        SELECT insurance_provider, ROUND(AVG(billing_amount),2) AS avg_bill
        FROM claim
        GROUP BY insurance_provider;
    """
    with get_connection() as conn:
        return pd.read_sql(sql, conn)

def patient_count_by_gender():
    sql = """
        SELECT gender, COUNT(*) AS count
        FROM patient
        GROUP BY gender;
    """
    with get_connection() as conn:
        return pd.read_sql(sql, conn)
