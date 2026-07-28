# Project Objectives

## Overview
This project predicts and analyzes CO2 adsorption behavior in Metal-Organic
Frameworks (MOFs) based on their physical and chemical properties, using
machine learning trained on simulated data and validated against real,
experimentally synthesized structures where possible.

## Phase 1 — Structure-Property Understanding
Use the hMOF simulated dataset (~32,768+ hypothetical MOF structures) to
identify which physical properties most strongly influence CO2 adsorption:
- Largest cavity diameter (LCD)
- Pore limiting diameter (PLD)
- Void fraction
- Surface area (m2/g)

This replicates and validates the structure-property relationships reported
in Wilmer et al., *Energy Environ. Sci.*, 2012 (DOI: 10.1039/C2EE23201D).

## Phase 2 — Ligand / Chemistry Effect
Extract functional group features (fluorine, chlorine, amine, etc.) from
the `mofid` SMILES field using RDKit, to determine how linker chemistry
affects CO2 uptake on top of pure pore geometry.

## Phase 3 — Bridge to Real MOFs (CoRE MOF)
Apply the model trained on hMOF (simulated) data to the CoRE MOF dataset
(real, experimentally synthesized structures) by feeding in their
structural properties (LCD, PLD, ASA_m2_g, AV_VF, etc.). This produces
predicted CO2 adsorption values for real, existing MOFs that do not have
measured adsorption data available.

## Phase 4 — Ground Truth Validation
For CoRE MOF structures that DO have experimental CO2 adsorption data
available (e.g. via NIST ISODB, matched by refcode), compare the model's
predictions against real measured values. This quantifies how well the
simulated-to-real transfer holds up, and grounds the project's conclusions
in experimental reality rather than simulation alone.

## Why This Matters
GCMC molecular simulation (the method used to generate the hMOF dataset)
is computationally expensive - hours per structure. A trained ML model
acts as a fast surrogate, allowing rapid screening of many candidate
structures. The end goal is not to treat simulated numbers as ground
truth, but to use them to learn structure-property patterns that can
guide experimental synthesis efforts toward promising real MOFs.