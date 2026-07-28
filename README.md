myproject/
├── .venv/                     # virtual environment (NOT committed)
│   ├── bin/
│   ├── include/
│   ├── lib/
│   ├── lib64/
│   ├── share/
│   └── pyvenv.cfg
├── configs/
│   └── config.yaml
├── data/
│   ├── processed/
│   └── raw/
├── notebook/
│   └── check_data.ipynb
├── src/
│   ├── app.py
│   ├── evaluate.py
│   ├── preprocess.py
│   └── train.py
├── tests/
│   ├── test_interface.py
│   ├── test_preprocess.py
│   └── test_model.py         
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt

=============================================================================
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
========================================================================
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

=============================================================================