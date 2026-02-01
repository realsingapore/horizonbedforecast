import pandas as pd
from sqlalchemy import text
from ..db import engine

def load_staffing(start_date=None, end_date=None):
    """
    Load staffing data from the database.
    Uses 'date' as the time column.
    """

    query = """
        SELECT *
        FROM staffing
        WHERE (:start_date IS NULL OR date >= :start_date)
          AND (:end_date IS NULL OR date < :end_date)
    """

    df = pd.read_sql(
        text(query),
        engine,
        params={"start_date": start_date, "end_date": end_date}
    )

    # Convert date column to datetime for consistency
    df["date"] = pd.to_datetime(df["date"])

    return df