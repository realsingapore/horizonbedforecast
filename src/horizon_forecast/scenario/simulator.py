# - Approach: Apply multipliers or overrides to key drivers, then re‑run model.

import pandas as pd

def apply_scenario(base_df: pd.DataFrame,
                   ed_multiplier=1.0,
                   elective_multiplier=1.0):
    df = base_df.copy()
    df["ed_arrivals_scn"] = df["ed_arrivals"] * ed_multiplier
    df["elective_surgeries_scn"] = df["elective_surgeries"] * elective_multiplier
    return df