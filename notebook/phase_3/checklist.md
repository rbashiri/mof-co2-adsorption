# Phase 3 — Metal-Node and Structure-Derived Descriptors

> **Question:** Can descriptors extracted directly from MOF structures improve CO₂ uptake prediction beyond the Phase 2 geometry + linker model?

## 3A — Match Structures to the Modeling Dataset

- [ ] Locate the CIF corresponding to each Phase 2 MOF record.
- [ ] Verify CIF–dataset matches using filename and available identifiers.
- [ ] Record missing, unreadable, and unmatched CIFs.
- [ ] Define the same matched MOF subset for baseline and new models.

## 3B — Extract Metal-Node Descriptors

- [ ] Identify metal elements present in each structure (for example, Zn, Cu, Co, Ni).
- [ ] Record the number of distinct metal elements per MOF.
- [ ] Define and record a reproducible metal-count measure; distinguish atom count from number of metal types.
- [ ] Add selected atomic properties, including atomic number and atomic mass.
- [ ] Investigate oxidation state and open metal sites; include a feature only where its assignment is reliable.
- [ ] Check extracted values against a sample of CIFs manually.

## 3C — Extract Additional Pore Descriptors

- [ ] Select structure-derived descriptors that add information beyond LCD, PLD, void fraction, and surface area.
- [ ] Calculate selected descriptors from CIFs using a documented tool and settings.
- [ ] Check units, missing values, and calculation failures.
- [ ] Keep only descriptors that can be calculated consistently for the matched subset.

## 3D — Controlled XGBoost Comparison

- [ ] Rebuild the Phase 2 geometry + linker baseline on the matched CIF subset.
- [ ] Train a second model with geometry + linkers + Phase 3 descriptors.
- [ ] Use identical rows, targets, model settings, and train/validation/test splits for both models.
- [ ] Check whether repeated or closely related structures cross the splits.
- [ ] Compare MAE, RMSE, and R² at all five CO₂ pressures.
- [ ] Quantify the improvement attributable to the added Phase 3 descriptor set.

## 3E — Interpretation and Literature

- [ ] Examine the importance of metal and new pore descriptors across pressures.
- [ ] Compare metal, linker, and geometry feature groups carefully.
- [ ] Investigate whether important descriptors have a scientifically plausible relationship to adsorption.
- [ ] Compare the findings with published MOF/CO₂ adsorption literature after metal testing.
- [ ] Document uncertainties, including unreliable oxidation-state or open-metal-site assignments.