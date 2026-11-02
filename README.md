# Project: Describe Health and Sleep Quality Data

## Project summary

This project computes descriptive statistics on the **Sleep Health and Lifestyle Dataset** (374 rows × 13 columns) and reports the findings in four slide-deck sections: a data description classifying variable types, the typical amount of physical activity, an analysis of daily steps taken, and the distribution of heart rates. A single reproducible Python script — `sleep_analysis.py` — downloads the CSV from the Udacity CDN, loads it with pandas, and executes every requested calculation in order: variable-type classification (Continuous → `Sleep Duration`, Integer → `Daily Steps`, Ordinal → `Quality of Sleep`, Nominal → `Gender`); measures of center for `Physical Activity Level` (mean **59.17**, median **60.00**, mode **60.00** — appearing in 70 of 374 records — indicating an approximately symmetric distribution, since mean ≈ median); measures of spread for `Daily Steps` (standard deviation **1617.92**, minimum **3000**, maximum **10000**, range **7000**, IQR **2400**, variance **2,617,651.14**); and a 15-bin histogram with KDE overlay for `Heart Rate` (mean **70.17**, median **70.00**), where the 1.5×IQR rule (fences at **62.00** and **78.00** bpm) identifies **15 outliers between 80 and 86 bpm**, revealing a right-skewed distribution (skewness **1.22**) with a secondary cluster in the mid-70s. All numbers are rounded to two decimal places and written to `analysis_summary.txt` under headers that match the four slide names; the figure is saved as `heart_rate_distribution.png` at 150 dpi.

## How to run

1. Install the dependencies (Python 3.14 verified; no other version constraints):

   ```bash
   pip install pandas numpy scipy matplotlib seaborn requests
   ```

2. Run the analysis from the project root:

   ```bash
   python sleep_analysis.py
   ```

   The script is idempotent: if `sleep_health.csv` already exists it is reused instead of re-downloaded, and the PNG/TXT outputs are overwritten with identical results.

3. Outputs land in the current working directory:
   - `heart_rate_distribution.png` — the distribution plot (150 dpi)
   - `analysis_summary.txt` — all computed values under the four slide headers

## Data sources

- **Sleep Health and Lifestyle Dataset** (Udacity CDN): <https://video.udacity-data.com/topher/2024/November/67325edd_sleep_health_and_lifestyle_dataset-sleep_health_and_lifestyle_dataset/sleep_health_and_lifestyle_dataset-sleep_health_and_lifestyle_dataset.csv>
- Original dataset on Kaggle: <https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset>

## Key results (copy into the slide deck)

| Slide | Result |
| :--- | :--- |
| **Data Description** | 374 rows × 13 columns; 219 blank `Sleep Disorder` cells (documented as "no disorder recorded"). Continuous → `Sleep Duration`; Integer → `Daily Steps`; Ordinal → `Quality of Sleep`; Nominal → `Gender`. |
| **Typical Physical Activity (Minutes)** | Mean 59.17 · Median 60.00 · Mode 60.00 (n = 70). Approximately symmetric: mean ≈ median. |
| **Analysis of Daily Steps Taken** | SD 1617.92 · Min 3000 · Max 10000 · Range 7000 · IQR 2400 · Variance 2,617,651.14. |
| **Distribution of Heart Rates** | Mean 70.17 · Median 70.00 · IQR fences 62.00/78.00 → 15 outliers (80–86 bpm). Right-skewed (skewness 1.22). |

## Rubric conformance

Reviewed against `docs/5. Rubric.md`, with every statistic independently recomputed in a second, separate implementation (Python `statistics` module + manual quartile interpolation) that matched the pandas/scipy results exactly:

| Rubric criterion | Status |
| :--- | :--- |
| Correct values for all statistical results | ✅ All values independently verified |
| Correct identification of variable types | ✅ One correct example per type |
| Measures of center and measures of spread provided when asked | ✅ 3 center measures, 6 spread measures |
| Heart rate distribution plotted, outliers identified | ✅ 15-bin histogram + KDE, IQR outliers listed |
| *Standout:* mean/median relationship → distribution shape | ✅ Stated for `Physical Activity Level` |
| *Standout:* multiple measures of center and spread | ✅ Mean/median/mode; SD/min/max/range/IQR/variance |

## Files

- `sleep_analysis.py` — the complete analysis script (Steps 1–7 of the project brief)
- `sleep_health.csv` — the downloaded dataset (374 × 13, 24,137 bytes)
- `heart_rate_distribution.png` — heart-rate histogram with KDE, mean/median lines (150 dpi)
- `analysis_summary.txt` — all computed results formatted under the four slide headers
- `docs/` — Udacity project documentation, rubric, and candidate notes
- `LICENSE.md` — project license

## Submission

The graded component is the slide deck (Google Slides or MS PowerPoint template — see `docs/3. Presentation Components.md`). The numbers in `analysis_summary.txt` map one-to-one to the four required slides and can be copied directly into the deck. Submission methods:

1. **Project Link**: submit the viewable link if you used the Google Slides template (make sure link access is set so anyone with the link can view).
2. **Single File**: submit the completed deck saved as a PDF if you used the MS PowerPoint template.
