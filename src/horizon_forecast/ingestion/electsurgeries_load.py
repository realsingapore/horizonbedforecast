import pandas as pd
from sqlalchemy import text
from ..db import engine

def load_elective_surgeries(start_date=None, end_date=None):
    query = """
        SELECT *
        FROM elective_surgeries
        WHERE (:start_date IS NULL OR surgery_date >= :start_date)
          AND (:end_date IS NULL OR surgery_date < :end_date)
    """

    df = pd.read_sql(
        text(query),
        engine,
        params={"start_date": start_date, "end_date": end_date}
    )

    df["surgery_date"] = pd.to_datetime(df["surgery_date"])
    return df