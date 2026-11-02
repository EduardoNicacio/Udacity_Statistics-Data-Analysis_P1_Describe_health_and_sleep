# Submission Notes

**Project:** Describe Health and Sleep Quality Data — Sleep Health and Lifestyle Dataset
**Program:** Udacity Statistics for Data Analysis Nanodegree
**Candidate:** Eduardo Nicacio
**Date:** November 2, 2026

These notes point to the files that matter most when reviewing this submission. Everything is in the project root unless stated otherwise.

---

## 1. Start here — the slide deck

**`analyze-sleep-health-and-lifestyle.pptx`** (project root, 7 slides) — the graded submission component, completed with all required results:

| Slide | Content | Rubric item |
| :--- | :--- | :--- |
| 1 | Title | — |
| 2 | Agenda | — |
| 3 | **Data Description** — dataset shape, columns, missingness, one example per variable type with justifications | Correct identification of variable types |
| 4 | **Typical Amount (Minutes) of Physical Activity** — mean 59.17, median 60.00, mode 60.00 + skewness interpretation | Measures of center; *standout:* mean/median → shape |
| 5 | **Analysis of Daily Steps Taken** — SD, min, max, range, plus IQR and variance | Measures of spread; *standout:* multiple measures |
| 6–7 | **Distribution of Heart Rates** — full statistics, IQR outliers (15 values, 80–86 bpm), shape description, and the distribution figure | Heart-rate plot + outliers |

Every number on the slides was copied from `analysis_summary.txt`, and the required plot is embedded on slide 7.

---

## 2. Key supporting files, in review order

| # | File | What it is | Why it matters |
| :--- | :--- | :--- | :--- |
| 1 | `analyze-sleep-health-and-lifestyle.pptx` | Completed slide deck (7 slides) | The graded artifact — see table above |
| 2 | `analysis_summary.txt` | All computed results under headers matching the four slide names | The single source for every figure on the slides; numbers can be copied directly into a deck |
| 3 | `heart_rate_distribution.png` | Histogram (15 bins) + KDE with dashed mean/median lines, 150 dpi | The plot the rubric requires; also embedded in the deck |
| 4 | `README.md` | Project overview, how to run, key-results table, rubric conformance | Fastest orientation: what was computed, how to re-run it, rubric status |
| 5 | `docs/6. Candidate Notes.md` | Full process notes: design decisions, AI collaboration, challenges, quality-gate results, findings verification, retrospective | Documents how the work was verified and why each decision was made (see especially §5 *Evaluation & Verification Philosophy* and §8 *Quality Gate Results*) |
| 6 | `sleep_analysis.py` | The complete analysis script (Steps 1–7) | Reproduces every number and both output files from the raw CSV |
| 7 | `sleep_health.csv` | Source dataset as downloaded (374 rows × 13 columns, 24,137 bytes) | The only data used — byte-for-byte from the Udacity CDN |
| 8 | `docs/5. Rubric.md` | The project rubric | Used for the self-review summarized below |

---

## 3. Rubric → evidence map

| Rubric criterion | Where to verify |
| :--- | :--- |
| All statistical values calculated correctly | `analysis_summary.txt` — every figure was independently recomputed in a second implementation (Python `statistics` module + manual quartiles) and matched at 2 decimals; see Candidate Notes §5 and §8 |
| Variable types correctly identified | Deck slide 3 / `analysis_summary.txt` → *Slide: Data Description* (Continuous → `Sleep Duration`, Integer → `Daily Steps`, Ordinal → `Quality of Sleep`, Nominal → `Gender`) |
| Measures of center / spread provided when asked | Deck slides 4–5 / summary: mean, median, mode; SD, min, max, range, IQR, variance |
| Heart-rate distribution plotted, outliers identified | `heart_rate_distribution.png` + deck slides 6–7: 15 outliers beyond the 62.00/78.00 IQR fences, shape described as right-skewed (skewness 1.22) |
| *Standout:* mean/median relationship → shape | Deck slide 4: mean 59.17 ≈ median 60.00 → approximately symmetric (confirmed by skewness 0.07) |
| *Standout:* multiple measures of center and spread | 3 center measures + 6 spread measures reported |

---

## 4. Reproduce in one command

```bash
python sleep_analysis.py
```

Re-runs are idempotent (the existing non-empty `sleep_health.csv` is reused) and regenerate `analysis_summary.txt` and `heart_rate_distribution.png` identically. Dependencies: `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn`, `requests` (Python 3.14 verified).

---

## 5. Data note

The dataset contains **219 blank `Sleep Disorder` cells** (58.6% of rows). Per the dataset documentation these mean "no disorder recorded"; they are disclosed on the Data Description slide and were **not** imputed or dropped — the column is unused by every statistic, so no reported figure is affected by the missingness.

---

*A summary of the submission artifacts for the Sleep Health and Lifestyle analysis; `analysis_summary.txt` is the source for all figures quoted in the deck.*
