## Phase 2 — Chemistry-Aware ML + RDKit

**Goal:** Add metal-node and linker chemistry descriptors to the Phase 1
geometric features and determine whether chemical information improves
CO₂ uptake prediction across different pressures.

## Phase 2 — Chemistry-Aware ML + RDKit

**Goal:** Add metal-node and linker chemistry descriptors to the Phase 1 geometric features and determine whether chemical information improves CO₂ uptake prediction across different pressures.

### 2A — Dataset Preparation

* [x] Assess MOFID availability

  * Total cleaned MOFs: 31,234
  * MOFID available: 27,706 (88.70%)
  * MOFID missing: 3,528 (11.30%)
* [x] Compare geometric properties of MOFID-present and MOFID-missing groups
* [x] Create chemistry subset containing 27,706 MOFs
* [ ] Document missing-MOFID limitation

#### 2A.1 — Chemistry-Subset Validation

Before chemistry extraction, validate and freeze the Phase 2 analysis dataset.

* [x] Confirm chemistry-subset shape

  * 27,706 rows
  * 11 columns
* [x] Confirm expected column names
* [x] Confirm missing MOFID count

  * Missing MOFID = 0
* [x] Count unique MOFIDs

  * Unique MOFIDs = 24,958
* [x] Check exact duplicate rows

  * Exact duplicate rows = 0
* [ ] Quantify repeated MOFID values
* [ ] Inspect repeated MOFIDs and determine which other columns differ
* [ ] Check missing values across all columns
* [ ] Verify column data types
* [ ] Check numeric columns for impossible or invalid values
* [ ] Confirm that the saved chemistry subset preserves the cleaned Phase 1 data
* [ ] Document validation results
* [ ] Freeze the Phase 2 chemistry-subset dataset before descriptor extraction

> **Important:** Repeated MOFID strings should not be removed automatically. First determine whether they correspond to distinct MOF records with different structural properties.

## Phase 2B — RDKit and MOFID Preparation
### RDKit Fundamentals

* [x] Learn essential RDKit concepts

  * [x] Atoms and element symbols
  * [x] Bonds and bond types
  * [x] Formal charges
  * [x] Aromatic atoms and bonds
  * [x] Implicit vs. explicit atoms

### MOFID Inspection and Parsing
* [x] Inspect representative complete MOFID strings
* [x] Parse MOFID chemical components
  * [x] Separate chemical representation from `MOFid-v1...` metadata
### Disconnected Fragment Representation
* [x] Determine how disconnected fragments are represented
  * [x] `.` separates disconnected components
  * [x] Fragment position does **not** reliably indicate chemical role
  * [x] Observed 1–14 fragments per MOF

### RDKit Parsing Assessment
* [x] Test RDKit parsing across the complete chemistry subset
  * [x] 25,952 MOFIDs tested
  * [x] 12,940 complete representations parsed successfully
  * [x] 13,012 failed standard RDKit parsing
### Investigation of Unparseable Representations

* [x] Investigate unparseable representations

  * [x] 12,284 of 13,012 failures contain `[Zn][O]([Zn])([Zn])[Zn]`
  * [x] Only 63 failed records carry the `ERROR` label
  * [x] Complete-MOF parsing failure does not necessarily mean the organic linker is invalid

### Fragmentation Analysis

* [x] Perform fragmentation analysis

  * [x] Split all chemical representations at `.`
  * [x] Count fragments per MOF
  * [x] Examine fragment positions 1–14
  * [x] Confirm that metals and organic components occur at different fragment positions

### Organic Linker and Metal-Component Separation 

* [ ] Separate organic linker(s) from metal-containing components

  * [ ] Identify metal-containing fragments
  * [ ] Identify remaining non-metal fragments
  * [ ] Distinguish candidate linkers from small/other components such as `N#N` and `N=N`
  * [ ] Define linker-selection rules

### Linker Extraction Validation

* [ ] Validate linker extraction

  * [ ] Test rules on representative MOFIDs
  * [ ] Apply rules across all 25,952 MOFs
  * [ ] Quantify MOFs with successful, ambiguous, and failed linker extraction

### Documentation

* [ ] Document final parsing rules and exclusions


### 2C — Metal-Node Descriptors

* [ ] Extract metal identity (Zn, Cu, Co, Ni, etc.)
* [ ] Determine number and type of metals
* [ ] Add selected metal atomic properties

  * Atomic number
  * Atomic mass
  * Other scientifically justified properties if needed
* [ ] Investigate metal oxidation state / valency

  * Include only when it can be assigned reliably

> **Note:** Open Metal Sites (OMS) will be investigated in Phase 3 using CIF/MOF-specific structural information rather than inferred from MOFID alone.

### 2D — Linker Descriptors

#### Elemental Composition

* [ ] Count C, N, O, F, S and other relevant elements
* [ ] Calculate heteroatom-related features

#### Functional Groups

* [ ] Identify relevant linker functional groups
* [ ] Investigate groups such as –NH₂, –OH, fluorinated groups, carboxylates and other polar functionalities

#### Physicochemical Descriptors

* [ ] Molecular weight
* [ ] Topological Polar Surface Area (TPSA)
* [ ] Hydrogen-bond donors (HBD)
* [ ] Hydrogen-bond acceptors (HBA)

#### Aromaticity

* [ ] Aromatic atom count
* [ ] Aromatic ring count
* [ ] Aromatic fraction

#### Linker Size and Geometry

* [ ] Heavy-atom count
* [ ] Ring count
* [ ] Rotatable-bond count
* [ ] Define a scientifically meaningful linker-length descriptor before calculating linker length

### 2E — Descriptor Validation

* [ ] Inspect descriptor distributions
* [ ] Check missing and invalid descriptor values
* [ ] Check constant / near-constant features
* [ ] Examine correlations and redundant descriptors
* [ ] Finalize chemistry feature set for modeling

### 2F — Controlled ML Comparison

* [ ] Use the same 27,706-MOF chemistry subset for both models
* [ ] Rebuild Geometry-Only Random Forest baseline

  * LCD
  * PLD
  * Void fraction
  * Surface area
* [ ] Build Geometry + Chemistry Random Forest
* [ ] Use identical train/validation/test splits for both models
* [ ] Compare MAE, RMSE and R² at:

  * 0.01 bar
  * 0.05 bar
  * 0.1 bar
  * 0.5 bar
  * 2.5 bar

### 2G — Explainability and Scientific Interpretation

* [ ] Run SHAP for the chemistry-aware model
* [ ] Compare geometry vs metal vs linker feature importance
* [ ] Examine how feature importance changes with pressure
* [ ] Determine whether chemistry provides greater improvement at low pressure
* [ ] Interpret important metal and linker descriptors scientifically
* [ ] Compare findings with published MOF/CO₂ adsorption literature

### Phase 2 Completion Criterion

Phase 2 is complete when the Geometry-Only and Geometry + Chemistry models have been evaluated on the same MOF subset and the contribution of chemical descriptors to CO₂ uptake prediction has been quantified and interpreted.


# ============================================================
# Phase 2A.1 — Chemistry Subset Validation
# ============================================================
Load → validate MOFID → check duplicates → investigate repeated MOFIDs → identify NA placeholders → remove NA → identify ERROR records → test ERROR records with RDKit.
``` python
import pandas as pd
from rdkit import Chem


# ------------------------------------------------------------
# 1. Load chemistry subset
# ------------------------------------------------------------

df = pd.read_csv(
    "/home/susan/mof-co2-adsorption/data/processed/df_chem.csv"
)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns)


# ------------------------------------------------------------
# 2. Check MOFID availability
# ------------------------------------------------------------

print("\nMissing MOFID:", df["mofid"].isna().sum())
print("Unique MOFID strings:", df["mofid"].nunique())


# ------------------------------------------------------------
# 3. Check exact duplicate rows
# ------------------------------------------------------------

print("\nExact duplicate rows:", df.duplicated().sum())


# ------------------------------------------------------------
# 4. Investigate repeated MOFID strings
# ------------------------------------------------------------

mofid_counts = df["mofid"].value_counts()

repeated_mofids = mofid_counts[mofid_counts > 1]

print("\nTotal rows:", len(df))
print("Unique MOFIDs:", df["mofid"].nunique())
print("Number of MOFID strings that repeat:", len(repeated_mofids))
print("Repeated occurrences:", df["mofid"].duplicated().sum())

print("\nMost frequent MOFIDs:")
print(mofid_counts.head())


# ------------------------------------------------------------
# 5. Identify unusable NA-type MOFID placeholders
# ------------------------------------------------------------

na_count = df["mofid"].str.contains(
    "MOFid-v1.NA", na=False
).sum()

print("\nNA-type MOFIDs:", na_count)


# ------------------------------------------------------------
# 6. Remove NA-type MOFID records
# ------------------------------------------------------------

df = df[
    ~df["mofid"].str.contains("MOFid-v1.NA", na=False)
].copy()

print("\nShape after removing NA-type MOFIDs:", df.shape)


# ------------------------------------------------------------
# 7. Recheck repeated MOFIDs after NA removal
# ------------------------------------------------------------

mofid_counts = df["mofid"].value_counts()

print("\nRepeated occurrences after NA removal:",
      df["mofid"].duplicated().sum())

print("\nMost frequent MOFIDs after NA removal:")
print(mofid_counts.head())


# ------------------------------------------------------------
# 8. Identify ERROR-type MOFIDs
# ------------------------------------------------------------

error_count = df["mofid"].str.contains(
    "MOFid-v1.ERROR", na=False
).sum()

print("\nERROR-type MOFIDs:", error_count)


# ------------------------------------------------------------
# 9. Test whether ERROR-type chemical strings can be
#    successfully parsed by RDKit
# ------------------------------------------------------------

error_mofids = df[
    df["mofid"].str.contains("MOFid-v1.ERROR", na=False)
]["mofid"]

parsed = 0
failed = 0

for mofid in error_mofids:

    # Extract chemical representation before MOFID metadata
    chemical_smiles = mofid.split(" ")[0]

    mol = Chem.MolFromSmiles(chemical_smiles)

    if mol is None:
        failed += 1
    else:
        parsed += 1


print("\nRDKit parsing of ERROR-type MOFIDs")
print("-----------------------------------")
print("Total ERROR records:", len(error_mofids))
print("Successfully parsed:", parsed)
print("Failed to parse:", failed)

```
