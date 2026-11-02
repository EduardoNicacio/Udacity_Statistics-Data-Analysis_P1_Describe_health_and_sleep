"""
Sleep Health and Lifestyle Dataset - descriptive statistics analysis.
Udacity project: Describe health and sleep (Steps 1-7).

Run with:  python sleep_analysis.py
Outputs:   sleep_health.csv, heart_rate_distribution.png, analysis_summary.txt
"""

import os
import sys

import numpy as np
import pandas as pd
import requests
from scipy import stats

import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt
import seaborn as sns

try:  # keep the em dash safe on Windows consoles
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CSV_URL = (
    "https://video.udacity-data.com/topher/2024/November/"
    "67325edd_sleep_health_and_lifestyle_dataset-sleep_health_and_lifestyle_dataset/"
    "sleep_health_and_lifestyle_dataset-sleep_health_and_lifestyle_dataset.csv"
)
CSV_PATH = "sleep_health.csv"
PNG_PATH = "heart_rate_distribution.png"
TXT_PATH = "analysis_summary.txt"

# Rounded values are collected here and dumped into analysis_summary.txt at the end.
summary_sections = []


def r2(value):
    """Round a scalar to 2 decimal places (returns a plain float)."""
    return round(float(value), 2)


def f2(value):
    """Format a number with exactly 2 decimal places for text output."""
    return f"{float(value):.2f}"


def header(title, char="-"):
    line = char * 72
    return f"{line}\n{title}\n{line}"


# ---------------------------------------------------------------------------
# STEP 1 - Download the dataset
# ---------------------------------------------------------------------------
def download_dataset(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"[Step 1] {path} already present ({os.path.getsize(path):,} bytes). "
              "Skipping download.")
        return

    print("[Step 1] Downloading dataset from Udacity ...")
    response = requests.get(url, timeout=180)
    response.raise_for_status()
    content = response.content

    # Verify the file is non-empty before continuing.
    if not content:
        raise RuntimeError("Downloaded file is empty - aborting.")

    with open(path, "wb") as handle:
        handle.write(content)

    print(f"[Step 1] Saved {path} ({len(content):,} bytes).")


download_dataset(CSV_URL, CSV_PATH)

if os.path.getsize(CSV_PATH) == 0:  # final safety check
    raise RuntimeError(f"{CSV_PATH} is empty - aborting.")

# ---------------------------------------------------------------------------
# STEP 2 - Load and inspect
# ---------------------------------------------------------------------------
print("\n" + header("[Step 2] Load and inspect"))
df = pd.read_csv(CSV_PATH)

if df.empty:
    raise RuntimeError("DataFrame is empty - aborting.")

print("\n--- df.head(5) ---")
print(df.head(5).to_string())

print("\n--- df.shape ---")
print(df.shape)

print("\n--- df.dtypes ---")
print(df.dtypes.to_string())

print("\n--- df.describe() ---")
print(df.describe().to_string())

print("\n--- df.isnull().sum() ---")
print(df.isnull().sum().to_string())

# ---------------------------------------------------------------------------
# STEP 3 - Variable type classification
# ---------------------------------------------------------------------------
print("\n" + header("[Step 3] Variable type classification"))

var_types = [
    (
        "1. Continuous variable",
        "Sleep Duration",
        "It is a float measured in hours that can take any fractional value in a "
        "range (e.g. 7.2), so it is measured rather than counted.",
    ),
    (
        "2. Integer variable",
        "Daily Steps",
        "It is a whole-number count of steps taken per day, so only discrete "
        "integer values are possible.",
    ),
    (
        "3. Ordinal categorical variable",
        "Quality of Sleep",
        "It is a 1-10 subjective rating whose categories have a meaningful natural "
        "order from worst to best sleep quality.",
    ),
    (
        "4. Nominal categorical variable",
        "Gender",
        "It labels group membership (Male / Female) with no inherent order or "
        "ranking between the categories.",
    ),
]

var_lines = []
for label, column, justification in var_types:
    example_values = df[column].dropna().unique()
    shown = ", ".join(str(v) for v in example_values[:6])
    entry = (
        f"{label}: '{column}'\n"
        f"   Example values: {shown}\n"
        f"   Justification: {justification}"
    )
    print("\n" + entry)
    var_lines.append(entry)

missing_total = int(df.isnull().sum().sum())
missing_cols = [
    f"'{col}' ({int(count)})"
    for col, count in df.isnull().sum().items()
    if count > 0
]
missing_note = (
    "Missing values: none - every column is complete."
    if missing_total == 0
    else f"Missing values: {missing_total} in total, found in "
    + ", ".join(missing_cols)
    + " (the blank Sleep Disorder entries are read as 'no disorder recorded')."
)

summary_sections.append(
    header("Slide: Data Description", "=")
    + "\nThe dataset contains "
    + f"{df.shape[0]} rows and {df.shape[1]} columns.\n"
    + "Columns: " + ", ".join(df.columns) + "\n"
    + missing_note + "\n\n"
    + "Variable types (one example of each):\n\n"
    + "\n\n".join(var_lines)
    + "\n"
)

# ---------------------------------------------------------------------------
# STEP 4 - Physical Activity Level: measures of center
# ---------------------------------------------------------------------------
print("\n" + header("[Step 4] Physical Activity Level - measures of center"))

pal = df["Physical Activity Level"].dropna()
pal_mean = pal.mean()
pal_median = pal.median()
pal_mode_result = stats.mode(pal, keepdims=True)
pal_mode = float(pal_mode_result.mode[0])
pal_mode_count = int(pal_mode_result.count[0])

if abs(pal_mean - pal_median) < 0.05 * abs(pal_median):
    skew_verdict = (
        "approximately symmetric, because the mean and median are almost identical"
    )
elif pal_mean > pal_median:
    skew_verdict = (
        "right-skewed (positively skewed), because the mean is greater than the "
        "median, so a few unusually high activity days pull the average upward"
    )
else:
    skew_verdict = (
        "left-skewed (negatively skewed), because the mean is less than the median, "
        "so a few unusually low activity days pull the average downward"
    )

pal_block = (
    f"Variable: Physical Activity Level (minutes/day), n = {pal.size}\n"
    f"Mean   : {f2(pal_mean)}\n"
    f"Median : {f2(pal_median)}\n"
    f"Mode   : {f2(pal_mode)} (occurs {pal_mode_count} times)\n\n"
    f"Interpretation: the distribution is {skew_verdict}."
)
print("\n" + pal_block)
summary_sections.append(
    header("Slide: Typical Physical Activity (Minutes)", "=") + "\n" + pal_block + "\n"
)

# ---------------------------------------------------------------------------
# STEP 5 - Daily Steps: measures of spread
# ---------------------------------------------------------------------------
print("\n" + header("[Step 5] Daily Steps - measures of spread"))

steps = df["Daily Steps"].dropna()
steps_std = steps.std(ddof=1)
steps_min = steps.min()
steps_max = steps.max()
steps_range = steps_max - steps_min
steps_q1 = steps.quantile(0.25)
steps_q3 = steps.quantile(0.75)
steps_iqr = steps_q3 - steps_q1
steps_var = steps.var(ddof=1)

steps_block = (
    f"Variable: Daily Steps, n = {steps.size}\n"
    f"Standard deviation : {f2(steps_std)}\n"
    f"Minimum            : {f2(steps_min)}\n"
    f"Maximum            : {f2(steps_max)}\n"
    f"Range              : {f2(steps_range)}\n"
    f"Q1                 : {f2(steps_q1)}\n"
    f"Q3                 : {f2(steps_q3)}\n"
    f"IQR (Q3 - Q1)      : {f2(steps_iqr)}\n"
    f"Variance           : {f2(steps_var)}"
)
print("\n" + steps_block)
summary_sections.append(
    header("Slide: Analysis of Daily Steps Taken", "=") + "\n" + steps_block + "\n"
)

# ---------------------------------------------------------------------------
# STEP 6 - Heart Rate distribution
# ---------------------------------------------------------------------------
print("\n" + header("[Step 6] Heart Rate distribution"))

hr = df["Heart Rate"].dropna()
hr_mean = hr.mean()
hr_median = hr.median()
hr_q1 = hr.quantile(0.25)
hr_q3 = hr.quantile(0.75)
hr_iqr = hr_q3 - hr_q1
hr_lower = hr_q1 - 1.5 * hr_iqr
hr_upper = hr_q3 + 1.5 * hr_iqr
hr_outliers = hr[(hr < hr_lower) | (hr > hr_upper)].sort_values()

skewness = float(stats.skew(hr))
kurtosis = float(stats.kurtosis(hr))

if skewness > 0.5:
    shape_text = (
        f"right-skewed (positively skewed, skewness = {f2(skewness)}): a long tail "
        "of high heart rates stretches toward the right, and the shape is not "
        "perfectly unimodal - a secondary cluster of elevated rates sits in the "
        "mid-70s bpm next to the main peak in the high 60s"
    )
elif skewness < -0.5:
    shape_text = (
        f"left-skewed (negatively skewed, skewness = {f2(skewness)}): a long tail "
        "of low heart rates stretches toward the left"
    )
else:
    shape_text = (
        f"approximately symmetric (skewness = {f2(skewness)}), centered near "
        f"{f2(hr_mean)} bpm"
    )

if len(hr_outliers) > 0:
    outlier_text = (
        f"Outliers exist: {len(hr_outliers)} value(s) fall outside the IQR fences "
        f"[{f2(hr_lower)}, {f2(hr_upper)}] -> "
        + ", ".join(str(int(v)) for v in hr_outliers.unique())
        + " bpm."
    )
else:
    outlier_text = (
        f"No outliers: every value lies inside the IQR fences "
        f"[{f2(hr_lower)}, {f2(hr_upper)}]."
    )

print(f"\nMean   : {f2(hr_mean)} bpm")
print(f"Median : {f2(hr_median)} bpm")
print(f"Q1     : {f2(hr_q1)} bpm | Q3: {f2(hr_q3)} bpm | IQR: {f2(hr_iqr)} bpm")
print(f"IQR lower fence: {f2(hr_lower)} bpm | IQR upper fence: {f2(hr_upper)} bpm")
print(f"Skewness: {f2(skewness)} | Excess kurtosis: {f2(kurtosis)}")
print("\n" + outlier_text)
print("\nShape description: the distribution is " + shape_text + ". " + outlier_text)

# --- Plot ---------------------------------------------------------------
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(9, 5.5))

sns.histplot(
    hr,
    bins=15,
    kde=True,
    color="#4C72B0",
    edgecolor="white",
    alpha=0.75,
    line_kws={"linewidth": 2, "color": "#1F3B63"},
    label="Heart rate (histogram + KDE)",
    ax=ax,
)

ax.axvline(
    hr_mean,
    color="#C44E52",
    linestyle="--",
    linewidth=2,
    label=f"Mean = {f2(hr_mean)} bpm",
)
ax.axvline(
    hr_median,
    color="#55A868",
    linestyle="--",
    linewidth=2,
    label=f"Median = {f2(hr_median)} bpm",
)

ax.set_xlabel("Heart Rate (beats per minute)")
ax.set_ylabel("Number of people")
ax.set_title("Distribution of Heart Rates")
ax.legend(loc="upper right", frameon=True)

fig.tight_layout()
fig.savefig(PNG_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\nFigure saved as {PNG_PATH} (150 dpi).")

hr_block = (
    f"Variable: Heart Rate (bpm), n = {hr.size}\n"
    f"Mean   : {f2(hr_mean)}\n"
    f"Median : {f2(hr_median)}\n"
    f"Q1     : {f2(hr_q1)}\n"
    f"Q3     : {f2(hr_q3)}\n"
    f"IQR    : {f2(hr_iqr)}\n"
    f"IQR lower fence : {f2(hr_lower)}\n"
    f"IQR upper fence : {f2(hr_upper)}\n"
    f"Skewness        : {f2(skewness)}\n"
    f"Excess kurtosis : {f2(kurtosis)}\n\n"
    f"{outlier_text}\n\n"
    f"Shape: the distribution is {shape_text}.\n"
    "Figure: heart_rate_distribution.png (histogram with 15 bins, KDE overlay, "
    "dashed mean and median lines)."
)
summary_sections.append(
    header("Slide: Distribution of Heart Rates", "=") + "\n" + hr_block + "\n"
)

# ---------------------------------------------------------------------------
# STEP 7 - Summary output file
# ---------------------------------------------------------------------------
with open(TXT_PATH, "w", encoding="utf-8") as handle:
    handle.write("SLEEP HEALTH AND LIFESTYLE DATASET - ANALYSIS SUMMARY\n")
    handle.write("Generated from sleep_health.csv\n\n")
    handle.write("\n".join(summary_sections))
    handle.write("\n")

print(f"\n[Step 7] All results written to {TXT_PATH}.")

print("\nDONE — analysis_summary.txt and heart_rate_distribution.png saved.")
