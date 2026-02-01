import pandas as pd
from sqlalchemy import text
from ..db import engine


def load_bed_inventory(start_date=None, end_date=None) -> pd.DataFrame:
    """
    Load bed inventory data from the database.

    Parameters:
        start_date (str or datetime, optional): Filter for records on or after this date.
        end_date (str or datetime, optional): Filter for records before this date.

    Returns:
        pd.DataFrame: Bed inventory data with datetime, ward, bed_type, and bed counts.
    """
    query = """
        SELECT *
        FROM bed_inventory
        WHERE (:start_date IS NULL OR datetime >= :start_date)
          AND (:end_date IS NULL OR datetime < :end_date)
    """

    df = pd.read_sql(text(query), engine, params={"start_date": start_date, "end_date": end_date})
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df