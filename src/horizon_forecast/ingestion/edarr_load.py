import pandas as pd
from sqlalchemy import text
from ..db import engine

def load_ed_arrivals(start_date=None, end_date=None):
    query = """
        SELECT *
        FROM ed_arrivals
        WHERE (:start_date IS NULL OR arrival_datetime >= :start_date)
          AND (:end_date IS NULL OR arrival_datetime < :end_date)
    """
    df = pd.read_sql(text(query), engine, params={"start_date": start_date, "end_date": end_date})
    df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"])
    return df