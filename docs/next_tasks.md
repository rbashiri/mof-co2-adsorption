# Next Session Tasks

## 1. Move parse_one_mof() into src/preprocess.py
- Copy the tested function from the notebook into src/preprocess.py
- Keep the notebook as the exploration/testing space only
- Confirm src/preprocess.py can be imported and run standalone:
  python3 src/preprocess.py path/to/sample.json

## 2. Copy the JSON folder locally (speed fix)
- External drive + WSL is slow for many small files (~21 min for 32,768 files)
- Copy once to local disk to speed up all future runs:
  mkdir -p ~/MOF_project/data/raw/hmof_json_local
  cp -r "/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db"/* ~/MOF_project/data/raw/hmof_json_local/
- Check disk space before copying:
  du -sh "/mnt/d/MOf/hMOF-10 1039 C2EE23201D-CarbonDioxide-mofdb-version_dc8a0295db"
  df -h ~
- Update notebook json_folder path to point to the local copy afterward

## 3. Add RDKit features (Phase 2)
- Use src/rdkit_features.py (already written and tested on 2 sample MOFs)
- Test on the same 20-file sample batch first before running on all 32,768
- Merge chemistry features (has_F, has_Cl, has_amine, mol_weight_avg, etc.)
  into the structural + CO2 dataset from Phase 1
- Handle the ~25% of rows with missing mofid (decide: drop vs keep as
  missing/False for chemistry columns)

## 4. Data cleaning
- Load data/raw/hmof_full_structural_co2.csv
- Check for missing values (df.isna().sum())
- Check for duplicate rows (df.duplicated().sum())
- Investigate rows with surface_area_m2g = 0 (seen in test batch, e.g. hMOF-10002)
  -> decide if these are valid (non-porous structures) or should be dropped
- Check for outliers in lcd, pld, void_fraction, surface_area_m2g
- Decide how to handle missing mofid rows

## 5. Exploratory Data Analysis (EDA)
- Distribution plots for lcd, pld, void_fraction, surface_area_m2g
- Distribution of CO2 uptake at each pressure (0.01, 0.05, 0.1, 0.5, 2.5 bar)
- Correlation matrix between structural features and CO2 uptake
- Scatter plots: surface_area vs CO2 uptake, void_fraction vs CO2 uptake
  (compare against the patterns reported in Wilmer et al. 2012, Fig. 1-3)
- Once RDKit features are added: compare CO2 uptake for has_F=True vs False
  (paper found fluorinated linkers performed best)

## Reference
See docs/PROJECT_OBJECTIVES.md for the full 4-phase project plan.
This session's work = Phase 1 (structure-property data), now moving into
cleaning/EDA before Phase 2 (chemistry features).