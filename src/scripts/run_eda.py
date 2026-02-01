import os
from pathlib import Path
import pandas as pd

from horizon_forecast.ingestion.adm_load import load_admissions
from horizon_forecast.ingestion.bedinv_load import load_bed_inventory
from horizon_forecast.ingestion.edarr_load import load_ed_arrivals
from horizon_forecast.ingestion.electsurgeries_load import load_elective_surgeries
from horizon_forecast.ingestion.staff_load import load_staffing

from horizon_forecast.forecasting.eda.eda_core import (
    eda_admissions_over_time,
    eda_admissions_by_type,
    eda_length_of_stay,
    eda_admissions_seasonality,
    eda_bed_inventory,
    eda_ed_arrivals_over_time,
    eda_elective_surgeries,
    eda_staffing_levels,
)




def main():
    print("Loading datasets...")

    admissions = load_admissions()
    bed_inventory = load_bed_inventory()
    ed_arrivals = load_ed_arrivals()
    elective_surgeries = load_elective_surgeries()
    staffing = load_staffing()

    # Ensure datetime fields
    admissions["admission_datetime"] = pd.to_datetime(admissions["admission_datetime"])
    ed_arrivals["arrival_datetime"] = pd.to_datetime(ed_arrivals["arrival_datetime"])
    elective_surgeries["surgery_date"] = pd.to_datetime(elective_surgeries["surgery_date"])
    bed_inventory["datetime"] = pd.to_datetime(bed_inventory["datetime"])
    staffing["date"] = pd.to_datetime(staffing["date"])

    print("Running EDA...")

    # Admissions
    eda_admissions_over_time(admissions)
    eda_admissions_by_type(admissions)
    eda_length_of_stay(admissions)
    eda_admissions_seasonality(admissions)

    # Bed Inventory
    eda_bed_inventory(bed_inventory)

    # ED Arrivals
    eda_ed_arrivals_over_time(ed_arrivals)

    # Elective Surgeries
    eda_elective_surgeries(elective_surgeries)

    # Staffing
    eda_staffing_levels(staffing)

    print("EDA complete. Figures saved to reports/figures.")


if __name__ == "__main__":
    main()
