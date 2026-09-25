# Phase 2 Extended Linker Descriptors

## Summary

This step extends the Phase 2 linker chemistry dataset by calculating additional RDKit-based chemical descriptors from the extracted linker SMILES.

The goal is to create MOF-level chemistry features that can later be combined with geometry features (`lcd`, `pld`, `void_fraction`, `surface_area_m2g`) to test whether linker chemistry improves CO2 uptake prediction.

Input dataset:

```text
data/processed/hmof_linker_extracted.csv