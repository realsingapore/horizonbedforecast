import pandas as pd


# ---------------------------------------------------------
# Helper: ensure a continuous date index
# ---------------------------------------------------------
def _ensure_date_index(df: pd.DataFrame, date_col: str, freq="D"):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()

    full_index = pd.date_range(df.index.min(), df.index.max(), freq=freq)
    df = df.reindex(full_index)

    df.index.name = date_col
    return df


# ---------------------------------------------------------
# Admissions aggregation
# ---------------------------------------------------------
def aggregate_admissions(adm_df: pd.DataFrame, freq="D"):
    df = adm_df.copy()

    # FIX: enforce datetime conversion
    df["admission_datetime"] = pd.to_datetime(df["admission_datetime"], errors="coerce")

    df["date"] = df["admission_datetime"].dt.floor(freq)

    ts = df.groupby("date").size().reset_index(name="admissions")
    ts = _ensure_date_index(ts, "date", freq)
    return ts


# ---------------------------------------------------------
# ED arrivals aggregation
# ---------------------------------------------------------
def aggregate_ed_arrivals(ed_df: pd.DataFrame, freq="D"):
    df = ed_df.copy()

    df["arrival_datetime"] = pd.to_datetime(df["arrival_datetime"], errors="coerce")

    df["date"] = df["arrival_datetime"].dt.floor(freq)

    ts = df.groupby("date").size().reset_index(name="ed_arrivals")
    ts = _ensure_date_index(ts, "date", freq)
    ts["ed_arrivals"] = ts["ed_arrivals"].fillna(0)

    return ts


# ---------------------------------------------------------
# Elective surgeries aggregation
# ---------------------------------------------------------
def aggregate_elective_surgeries(elec_df: pd.DataFrame, freq="D"):
    df = elec_df.copy()

    df["surgery_date"] = pd.to_datetime(df["surgery_date"], errors="coerce")
    
    df["date"] = df["surgery_date"].dt.floor(freq)

    ts = df.groupby("date").size().reset_index(name="elective_surgeries")
    ts = _ensure_date_index(ts, "date", freq)
    ts["elective_surgeries"] = ts["elective_surgeries"].fillna(0)

    return ts


# ---------------------------------------------------------
# Bed inventory aggregation
# ---------------------------------------------------------
def aggregate_bed_inventory(bed_df: pd.DataFrame):
    df = bed_df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date

    ts = df.groupby(["date", "ward"])["total_beds"].mean().reset_index()
    ts["date"] = pd.to_datetime(ts["date"])

    return ts


# ---------------------------------------------------------
# Staffing aggregation
# ---------------------------------------------------------
def aggregate_staffing(staff_df: pd.DataFrame, freq="D"):
    df = staff_df.copy()
    df["date"] = pd.to_datetime(df["date"])

    ts = df.groupby(["date", "ward"])["actual_staff"].mean().reset_index()
    ts["date"] = pd.to_datetime(ts["date"])

    return ts


# ---------------------------------------------------------
# Unified demand signal
# ---------------------------------------------------------
def build_demand_timeseries(adm, ed, elec, freq="D"):
    """
    Combine all demand drivers into a single modeling-ready dataframe.
    """

    adm_ts = aggregate_admissions(adm, freq)
    ed_ts = aggregate_ed_arrivals(ed, freq)
    elec_ts = aggregate_elective_surgeries(elec, freq)

    df = adm_ts.join(ed_ts, how="outer").join(elec_ts, how="outer")
    df = df.fillna(0)

    # Add calendar features
    df["dow"] = df.index.dayofweek
    df["month"] = df.index.month
    df["is_weekend"] = df["dow"].isin([5, 6]).astype(int)

    return df