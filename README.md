## Project Structure

```text
myproject/
├── .venv/                     # Virtual environment (not committed)
├── configs/
│   └── config.yaml
├── data/
│   ├── processed/
│   └── raw/
├── docs/
│   └── PROJECT_OBJECTIVES.md
├── notebook/
│   └── check_data.ipynb
├── src/
│   ├── app.py
│   ├── evaluate.py
│   ├── preprocess.py
│   └── train.py
├── tests/
│   ├── test_interface.py
│   ├── test_model.py
│   └── test_preprocess.py
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```
====================================================
## Project Objectives
### Overview
This project predicts and analyzes CO2 adsorption behavior in Metal-Organic
Frameworks (MOFs) based on their physical and chemical properties, using
machine learning trained on simulated data and validated against real,
experimentally synthesized structures where possible.

###  Phase 1 — Structure-Property Understanding
Use the hMOF simulated dataset (~32,768+ hypothetical MOF structures) to
identify which physical properties most strongly influence CO2 adsorption:
- Largest cavity diameter (LCD)
- Pore limiting diameter (PLD)
- Void fraction
- Surface area (m2/g)

This replicates and validates the structure-property relationships reported
in Wilmer et al., *Energy Environ. Sci.*, 2012 (DOI: 10.1039/C2EE23201D).

See [docs/PROJECT_OBJECTIVES.md](docs/PROJECT_OBJECTIVES.md) for the full multi-phase plan.
======================================================
## project Dataset

**Source:** hMOF (hypothetical Metal-Organic Framework) database,
originating from Wilmer et al., *Energy Environ. Sci.*, 2012
(DOI: 10.1039/C2EE23201D), accessed via the mofdb bulk download.

**File type used:** `.json` (not `.cif`)

**Why JSON over CIF:**
- The `.cif` files contain only raw crystallographic data (unit cell
  parameters and atomic coordinates) — using them would require running
  separate pore-analysis software (e.g. Zeo++) to compute structural
  descriptors from scratch.
- The `.json` files already include the pre-computed structural properties
  (`lcd`, `pld`, `void_fraction`, `surface_area_m2g`) **and** simulated
  gas adsorption isotherms (CO2, N2, CH4) at multiple pressures — giving
  both the input features (X) and the prediction target (Y) needed for
  this project without extra preprocessing.
- `.cif` files are retained on external storage in case future work
  requires custom structural feature extraction beyond what's in the JSON.

**Fields extracted per MOF:**
| Field | Description |
|---|---|
| `lcd` | Largest cavity diameter (Å) |
| `pld` | Pore limiting diameter (Å) |
| `void_fraction` | Fraction of accessible void volume |
| `surface_area_m2g` | Gravimetric surface area (m²/g) |
| `elements` | Constituent atoms in the framework |
| `isotherms` | CO2 (and N2/CH4) adsorption uptake (mol/kg) at multiple pressures, 298 K |

**Dataset size:** ~50,000 hMOF structures (JSON + paired CIF files)
======================================================
## CO2 Uptake Columns

The dataset includes CO2 adsorption values measured at five different
gas pressures, from the same simulated MOF structure — not five
different properties.

| Column | Meaning |
|---|---|
| `CO2_uptake_0.01bar_molkg` | CO2 adsorbed at very low pressure (0.01 bar) |
| `CO2_uptake_0.05bar_molkg` | CO2 adsorbed at 0.05 bar |
| `CO2_uptake_0.1bar_molkg` | CO2 adsorbed at 0.1 bar |
| `CO2_uptake_0.5bar_molkg` | CO2 adsorbed at 0.5 bar |
| `CO2_uptake_2.5bar_molkg` | CO2 adsorbed at 2.5 bar (highest pressure tested) |

**Why pressure matters:** at low pressure, only MOFs with strong CO2-binding sites (e.g. open metal sites, polar functional groups) adsorb meaningfully weaker materials adsorb almost nothing. At high pressure, CO2 is pushed into any available pore space, so uptake becomes driven more by physical capacity (surface area, pore volume) than by binding strength.

This mirrors why Wilmer et al. (2012) evaluated four separate industrial
cases at different pressures: flue gas capture occurs at low CO2 partial
pressure (~0.1 bar), while natural gas purification occurs at higher
pressure — so the "best" MOF depends on which pressure regime matters
for the target application.

**Implication for feature importance:** the most influential structural or
chemical property can differ depending on which pressure column is analyzed.
For example, void fraction may matter more at 2.5 bar (physical space
dominates), while chemistry-based features (e.g. fluorine content, once
added via RDKit) may matter more at 0.01 bar (binding strength dominates).
Correlation and feature-importance analysis should therefore be checked
across all five pressure columns, not just one.

======================================================
## Data Cleaning Summary

- Loaded the dataset and inspected its structure, including shape, columns, and sample records.
- Standardized column names by removing extra whitespace, converting them to lowercase, and replacing spaces with underscores.
- Identified and summarized missing values by column.
- Reviewed rows with missing mofid values to assess data quality.
- Checked for duplicate records and counted them.
- Investigated rows with zero surface area and removed those with both zero surface area and missing mofid.
- Rechecked the remaining missing values after filtering.
- Explored potential outliers using descriptive statistics, boxplots, and the IQR method for key numeric features.

Note: The remaining hMOF entries will be kept even though the mofid is null. No further action was taken on this decision.




======================================================
## Feature and Target Selection

The project uses structural properties to predict CO₂ uptake.
The variables are assigned the following roles:

| Role | Variables | Purpose |
|------|-----------|---------|
| **Features (`X`)** | `lcd`, `pld`, `void_fraction`, `surface_area_m2g` | Describe the pore structure and physical properties of each MOF |
| **Targets (`y`)** | Five CO₂-uptake columns | Measure CO₂ adsorption at different pressures |
| **Identifiers** | `filename`, `mofid` | Identify and trace individual records |

> `filename` and `mofid` are excluded from model features — they are
> identifiers, not physical MOF properties.  
> Missing `mofid` values do not affect the current analysis because all
> required feature and target values are complete.

---

### Recommended Modeling Approach: Separate Regression by Pressure

A separate regression model will be trained for each CO₂-pressure target:

| Model | Target |
|-------|--------|
| Model 1 | `CO2_uptake_0.01bar_molkg` |
| Model 2 | `CO2_uptake_0.05bar_molkg` |
| Model 3 | `CO2_uptake_0.1bar_molkg` |
| Model 4 | `CO2_uptake_0.5bar_molkg` |
| Model 5 | `CO2_uptake_2.5bar_molkg` |

This approach makes it possible to compare how the influence of `lcd`,
`pld`, `void_fraction`, and `surface_area_m2g` changes across pressure
regimes:

- At **low pressure** (0.01 – 0.1 bar), CO₂ adsorption is more sensitive
  to pore accessibility and chemical interactions — relevant to **flue gas
  capture** (~0.1 bar CO₂ partial pressure).
- At **high pressure** (0.5 – 2.5 bar), physical capacity dominates —
  void fraction and surface area become more influential — relevant to
  **natural gas purification**.

> ⚠️ These relationships will be tested using **correlation analysis** and
> **model-based feature importance** rather than assumed in advance.
> Feature importance should be checked across all five pressure targets,
> not just one, consistent with the approach in Wilmer et al. (2012).


======================================================
## Exploratory Data Analysis (EDA)

EDA is performed before modeling to understand the structure of the data,
confirm expected physical relationships, and identify any patterns that
should inform modeling decisions.

### EDA Priorities

| Priority | Analysis | Purpose |
|----------|----------|---------|
| 1 | **Target distributions** | Compare the range, skewness, and zeros of CO₂ uptake at each pressure |
| 2 | **Pearson and Spearman correlations** | Measure linear and monotonic feature–uptake relationships |
| 3 | **Scatter / hexbin plots** | Identify nonlinear relationships and feature interactions |
| 4 | **Feature-to-feature correlations** | Detect strongly related predictors such as `lcd` and `pld` |
| 5 | **Outlier sensitivity** | Check whether flagged MOFs change the observed relationships |

### EDA Order

1. Examine the five CO₂ target distributions 
2. Calculate Pearson and Spearman correlations
3. Visualize the strongest feature–target relationships
4. Compare results with and without flagged outliers
5. Begin regression modeling and feature importance

---

### Why This Order

**Step 1** establishes whether the targets are normally distributed,
heavily skewed, or contain zero-uptake MOFs — this affects which
correlation method and model type is appropriate.

**Step 2** uses two correlation methods intentionally:
- **Pearson** measures linear relationships — appropriate if features and
  targets scale proportionally.
- **Spearman** measures monotonic relationships — more robust when
  distributions are skewed or contain outliers, which is expected here
  given the IQR results.

**Step 3** visualizes the strongest correlations found in Step 3 to
confirm whether relationships are truly linear or follow a nonlinear
pattern — this informs whether a linear model or tree-based model is
more suitable.

**Step 4** repeats key correlations after removing the 619 low
`void_fraction` outliers and 688 large `lcd` outliers to confirm that
the observed relationships are not driven by extreme values.

**Step 5** begins only after EDA is complete, so that model choice,
feature scaling decisions, and interpretation of feature importance are
all grounded in observed data patterns rather than assumed in advance.

> This sequence is consistent with the analytical approach used in
> Wilmer et al. (2012), where structural descriptors were evaluated
> across multiple pressure regimes before drawing conclusions about
> which features drive CO₂ adsorption.

======================================================
