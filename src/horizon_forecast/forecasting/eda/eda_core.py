import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

FIG_DIR = Path("reports") / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save_fig(fig, name: str):
    path = FIG_DIR / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"[EDA] Saved: {path}")


# ---------------------------------------------------------
# ADMISSIONS EDA
# ---------------------------------------------------------

def eda_admissions_over_time(adm_df: pd.DataFrame, freq="D"):
    df = adm_df.copy()
    df["date"] = df["admission_datetime"].dt.floor(freq)

    ts = df.groupby("date").size().reset_index(name="admissions")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(ts["date"], ts["admissions"], linewidth=1.2)
    ax.set_title(f"Admissions Over Time ({freq})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Admissions")
    _save_fig(fig, f"admissions_over_time_{freq}")


def eda_admissions_by_type(adm_df: pd.DataFrame):
    df = adm_df.copy()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.countplot(data=df, x="admission_type", ax=ax)
    ax.set_title("Admissions by Type")
    ax.set_xlabel("Admission Type")
    ax.set_ylabel("Count")
    plt.xticks(rotation=30)
    _save_fig(fig, "admissions_by_type")


def eda_length_of_stay(adm_df: pd.DataFrame):
    df = adm_df.copy()
    df = df[df["length_of_stay_hours"].notna()]

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df["length_of_stay_hours"], bins=50, kde=True, ax=ax)
    ax.set_title("Length of Stay Distribution (Hours)")
    ax.set_xlabel("Length of Stay (Hours)")
    ax.set_ylabel("Count")
    _save_fig(fig, "length_of_stay_distribution")


def eda_admissions_seasonality(adm_df: pd.DataFrame):
    df = adm_df.copy()
    df["dow"] = df["admission_datetime"].dt.dayofweek
    df["month"] = df["admission_datetime"].dt.month

    fig, ax = plt.subplots(1, 2, figsize=(12, 4))

    sns.countplot(data=df, x="dow", ax=ax[0])
    ax[0].set_title("Admissions by Day of Week")

    sns.countplot(data=df, x="month", ax=ax[1])
    ax[1].set_title("Admissions by Month")

    _save_fig(fig, "admissions_seasonality")


# ---------------------------------------------------------
# BED INVENTORY EDA
# ---------------------------------------------------------

def eda_bed_inventory(bed_df: pd.DataFrame):
    df = bed_df.copy()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x="ward", y="total_beds", ax=ax)
    ax.set_title("Total Beds by Ward")
    plt.xticks(rotation=30)
    _save_fig(fig, "bed_inventory_by_ward")


# ---------------------------------------------------------
# EMERGENCY ARRIVALS EDA
# ---------------------------------------------------------

def eda_ed_arrivals_over_time(ed_df: pd.DataFrame, freq="D"):
    df = ed_df.copy()
    df["date"] = df["arrival_datetime"].dt.floor(freq)

    ts = df.groupby("date").size().reset_index(name="ed_arrivals")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(ts["date"], ts["ed_arrivals"], linewidth=1.2)
    ax.set_title(f"ED Arrivals Over Time ({freq})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Arrivals")
    _save_fig(fig, f"ed_arrivals_over_time_{freq}")


# ---------------------------------------------------------
# ELECTIVE SURGERIES EDA
# ---------------------------------------------------------

def eda_elective_surgeries(elec_df: pd.DataFrame):
    df = elec_df.copy()
    df["date"] = df["surgery_date"].dt.date

    ts = df.groupby("date").size().reset_index(name="surgeries")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(ts["date"], ts["surgeries"], linewidth=1.2)
    ax.set_title("Elective Surgeries Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Surgeries")
    _save_fig(fig, "elective_surgeries_over_time")


# ---------------------------------------------------------
# STAFFING EDA
# ---------------------------------------------------------

def eda_staffing_levels(staff_df: pd.DataFrame):
    df = staff_df.copy()

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x="ward", y="actual_staff", ax=ax)
    ax.set_title("Staffing Levels by Ward")
    plt.xticks(rotation=30)
    _save_fig(fig, "staffing_by_ward")