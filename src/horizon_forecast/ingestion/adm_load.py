import pandas as pd
from sqlalchemy import text
from ..db import engine


# ---------------------------------------------------------
# ADMISSIONS LOADER
# ---------------------------------------------------------

def load_admissions():
    query = "SELECT * FROM admissions"
    return pd.read_sql(text(query), engine)


# ---------------------------------------------------------
# BED INVENTORY LOADER
# ---------------------------------------------------------

def load_bed_inventory():
    query = "SELECT * FROM bed_inventory"
    return pd.read_sql(text(query), engine)


# ---------------------------------------------------------
# ED_ARRIVALS LOADER
# ---------------------------------------------------------

def load_ed_arrivals():
    query = "SELECT * FROM ed_arrivals"
    return pd.read_sql(text(query), engine)


# ---------------------------------------------------------
# ELECTIVE_SURGERIES LOADER
# ---------------------------------------------------------

def load_elective_surgeries():
    query = "SELECT * FROM elective_surgeries"
    return pd.read_sql(text(query), engine)


# ---------------------------------------------------------
# STAFFING LOADER
# ---------------------------------------------------------

def load_staffing():
    query = "SELECT * FROM staffing"
    return pd.read_sql(text(query), engine)


