# Phase 2 — MOFID Linker Extraction and Dataset Preparation

## Purpose and scope

This workflow prepares a linker-based chemistry dataset for testing whether linker descriptors improve CO₂ uptake predictions beyond LCD, PLD, void fraction, and surface area.

Linker extraction was not a single direct SMILES conversion. The work progressed from checking MOFID quality, through investigating whole-representation parsing failures, to disconnecting metal bonds and validating individual fragments. The final retention rule kept a MOF if at least one candidate linker survived the implemented filters and RDKit sanitization.

Metal-containing components were handled during extraction, but metal identity, metal counts, oxidation states, and metal-node descriptors were not added as modeling features. Those descriptors are outside the current Phase 2 scope.

Source: `rdkit_final_version.ipynb`, supplied on 21 September 2026. This document describes the saved code and outputs; the underlying dataset was not supplied or rerun for this review. Cell references below use notebook position, counted from 1, including Markdown cells.

---

## 1. Load and inspect the chemistry subset

The notebook loaded `data/processed/df_chem.csv` into `df`.

### Initial check

| Metric | Value |
| --- | ---: |
| Rows | 27,706 |
| Columns | 11 |
| Missing MOFID values | 0 |
| Unique MOFID strings | 24,958 |
| Exact duplicate rows | 0 |
| Extra occurrences of repeated MOFID strings | 2,748 |

The notebook also records 616 MOFID strings occurring more than once, with a maximum frequency of 1,259. Repeated MOFID strings were investigated rather than treated automatically as duplicate MOF records. No general MOFID-based deduplication step appears in the notebook.

The 11 initial columns were `filename`, `mofid`, the four geometry features, and five CO₂ uptake targets at 0.01, 0.05, 0.1, 0.5, and 2.5 bar.

---

## 2. Remove unavailable-MOFID placeholders

Two placeholder strings accounted for 1,754 records:

| Placeholder | Rows |
| --- | ---: |
| `* MOFid-v1.NA.NA` | 1,259 |
| `* MOFid-v1.NA.NA_no_mof` | 495 |
| Total | 1,754 |

The implemented filter was:

```python
df = df[
    ~df["mofid"].str.contains("MOFid-v1.NA", na=False)
].copy()
```

The resulting dataset contained 25,952 rows and 11 columns, with zero remaining matches to that filter. These 1,754 exclusions occurred before linker extraction and are separate from the later 23 exclusions.

---

## 3. Investigate `ERROR`-labelled MOFIDs

An `ERROR` metadata label was not used as an automatic exclusion rule. The notebook extracted the chemical portion before the first space and tested it using standard `Chem.MolFromSmiles()`.

### `ERROR`-labelled subset

| Category | Rows |
| --- | ---: |
| Total | 1,691 |
| Standard RDKit parsing succeeded | 1,628 |
| Standard RDKit parsing failed | 63 |

This showed that the metadata label alone was insufficient to determine whether the chemical representation could be read by RDKit. The 63 records were diagnostic failures at this stage, not a separate set of final exclusions.

---

## 4. Test complete chemical representations

The same standard parsing test was applied to all 25,952 remaining records.

### Complete-representation parsing

| Category | Rows |
| --- | ---: |
| Parsed | 12,940 |
| Failed | 13,012 |

A representative failed input was:

```text
[O-]C(=O)c1ccc(cc1)C(=O)[O-].[Zn][O]([Zn])([Zn])[Zn]
```

The complete representation returned `None`, while its first dot-separated organic fragment could be parsed independently. This motivated fragment-level processing instead of discarding every record whose complete representation failed.

Among the 13,012 failures, 12,284 contained the exact fragment `[Zn][O]([Zn])([Zn])[Zn]`, and 728 did not. This supported investigating the coordination-containing representations; it did not prove that the same fragment caused every failure.

Additional diagnostic counts among the failures were 63 containing `ERROR`, 7,210 containing `pcu.cat0`, 3,659 containing `pcu.cat1`, and 6 containing `N#N`. These counts describe overlapping patterns, not mutually exclusive exclusion categories.

---

## 5. Separate chemical content from MOFID metadata

The extraction workflow used:

```python
chemical_smiles = mofid.split("MOFid-v1")[0].strip()
```

The result was stored in `chemical_representation`, and a working copy named `df_fragments` was created. The original MOFID, structure identifier, geometry features, and uptake targets were retained.

---

## 6. Develop the metal-disconnection approach

The notebook first demonstrated the approach on the first MOF:

1. Read the chemical representation with `Chem.MolFromSmiles(chemical, sanitize=False)`.
2. Update cached properties with `UpdatePropertyCache(strict=False)`.
3. Apply `rdMolStandardize.MetalDisconnector().Disconnect()`.
4. Split the disconnected molecule into fragments.

The example returned one organic fragment, four zinc fragments, and an oxide fragment:

```text
O=C([O-])c1ccc(C(=O)[O-])cc1
[Zn+]
[O-2]
[Zn+]
[Zn]
[Zn]
```

The development step initially removed isolated metals and selected small inorganic fragments. The final function added exact exclusions for `[Zn][Zn]`, `[Cu][Cu]`, and `[O]`, and postponed fragment sanitization until after filtering.

The charges in this intermediate output were not used to assign metal oxidation states.

---

## 7. Final extraction and fragment-selection rules

The final `extract_linkers(chemical)` function is in source cell 32. It performs the following operations in order.

### 7.1 Read without initial sanitization

The function loads the full representation using `sanitize=False`. If RDKit cannot create a molecule at all, it raises an exception. Otherwise it updates the property cache with `strict=False`.

### 7.2 Disconnect and split

After metal disconnection, fragments are generated with:

```python
fragments = Chem.GetMolFrags(
    disconnected_mol,
    asMols=True,
    sanitizeFrags=False
)
```

This permits filtering and subsequent validation of individual candidates.

### 7.3 Remove isolated atoms using the configured atomic-number list

The implemented list contains atomic numbers 3–4, 11–13, 19–31, 37–50, 55–84, and 87–112. A fragment is removed by this rule only when it contains exactly one atom and that atom is in the list.

This is the exact configured list, not a claim that every element in those ranges is conventionally classified as a metal. The rule does not reject every multi-atom fragment containing a metal.

### 7.4 Remove selected small inorganic fragments

| SMARTS pattern | Intended exclusion |
| --- | --- |
| `[O-2]` | Oxide ion |
| `N#N` | Standalone nitrogen fragment |
| `[O;H2]` | Water |
| `[O-]S(=O)(=O)[O-]` | Sulfate |

A fragment must both match the pattern and have the same heavy-atom count as that pattern. This avoids removing an entire larger molecule merely because it contains a matching substructure.

There is no explicit `N=N` exclusion in the final function. It should not be documented as an implemented rule.

### 7.5 Remove exact standalone fragments

The exact SMILES blacklist is:

```python
exact_fragment_blacklist = {"[Zn][Zn]", "[Cu][Cu]", "[O]"}
```

This check is applied before and after candidate sanitization.

### 7.6 Sanitize surviving candidates individually

For each remaining fragment, the function calls `UpdatePropertyCache(strict=False)` and `Chem.SanitizeMol(frag)`. Successful candidates are converted to SMILES using `Chem.MolToSmiles()` and appended to `linker_smiles`.

If candidate sanitization fails, its SMILES and exception message are added to `invalid_fragments`; processing continues for the other candidates in that MOF.

The function returns:

```python
return linker_smiles, invalid_fragments
```

No manual, structure-specific charge or bond repairs are implemented in this final function. Metal disconnection and sanitization are themselves transformations, so the extracted fragments should not be described as unchanged copies of the complete framework representation.

---

## 8. Apply extraction to all 25,952 MOFs

The processing loop collects:

- `all_linkers`: retained candidate SMILES for each MOF
- `all_invalid_fragments`: rejected candidate SMILES and their errors
- `failed_linker_extraction`: original row index, chemical representation, and exception for complete extraction failures

When the entire function raises an exception, empty lists are appended for both output columns to preserve alignment with the original DataFrame. The exception is retained separately in `failed_linker_extraction`.

The loop processed 25,952 rows and recorded four complete extraction failures. A separate check of `len(linker_smiles) == 0` then identified 23 rows, showing that complete function failure was not the only reason a MOF lacked retained linkers.

---

## 9. Explain the 23 exclusions

| Exclusion category | Rows | Meaning |
| --- | ---: | --- |
| Complete extraction failure | 4 | The extraction function raised an exception |
| No retained candidate linker | 19 | The function returned, but every fragment was filtered out or failed candidate sanitization |
| Total excluded | 23 | `linker_smiles` was empty |

The notebook labels the second category as “all fragments excluded.” This category includes fragment sanitization failures; it does not mean that all 19 representations contained only inorganic material. The saved exclusion table shows invalid-fragment entries in 13 of these rows, while six have empty invalid-fragment lists and representations consisting of `N#N` plus a Zn or Cu dimer.

The four complete failures were:

| Original row index | MOF identifier | Recorded error |
| --- | --- | --- |
| 5616 | `hMOF-151` | Br atom 118: explicit valence 21 |
| 11070 | `hMOF-20326` | O atom 12: explicit valence 32 |
| 24142 | `hMOF-368` | O atom 41: explicit valence 32 |
| 27218 | `hMOF-6556` | O atom 17: explicit valence 3 |

The displayed messages report valences greater than permitted. The outputs do not contain a full traceback locating the exact failing operation within the function.

### Complete exclusion register

| Original row index | MOF identifier | Category |
| --- | --- | --- |
| 3023 | `hMOF-12739` | No retained candidate linker |
| 5616 | `hMOF-151` | Complete extraction failure |
| 8121 | `hMOF-17422` | No retained candidate linker |
| 10568 | `hMOF-19759` | No retained candidate linker |
| 10570 | `hMOF-19760` | No retained candidate linker |
| 10585 | `hMOF-19779` | No retained candidate linker |
| 10760 | `hMOF-19962` | No retained candidate linker |
| 11070 | `hMOF-20326` | Complete extraction failure |
| 11782 | `hMOF-21484` | No retained candidate linker |
| 13101 | `hMOF-22905` | No retained candidate linker |
| 14155 | `hMOF-23902` | No retained candidate linker |
| 14191 | `hMOF-23939` | No retained candidate linker |
| 14831 | `hMOF-24526` | No retained candidate linker |
| 15464 | `hMOF-25105` | No retained candidate linker |
| 17126 | `hMOF-26645` | No retained candidate linker |
| 19114 | `hMOF-28530` | No retained candidate linker |
| 21038 | `hMOF-30369` | No retained candidate linker |
| 22034 | `hMOF-31424` | No retained candidate linker |
| 24142 | `hMOF-368` | Complete extraction failure |
| 24228 | `hMOF-3757` | No retained candidate linker |
| 24617 | `hMOF-4107` | No retained candidate linker |
| 27218 | `hMOF-6556` | Complete extraction failure |
| 27393 | `hMOF-6716` | No retained candidate linker |

---

## 10. Create and check the retained dataset

The final selection was:

```python
df_chemistry = df_fragments[
    df_fragments["linker_smiles"].apply(len) > 0
].copy()
```

| Stage | Rows | Columns |
| --- | ---: | ---: |
| Input chemistry subset | 27,706 | 11 |
| After placeholder removal | 25,952 | 11 |
| After extraction and audit columns | 25,952 | 14 |
| After excluding empty linker lists | 25,929 | 14 |

The retention rate for the extraction stage was 99.91% (25,929 / 25,952). This is a row-level retention rate, not a measurement of chemical identification accuracy.

The three added columns were `chemical_representation`, `linker_smiles`, and `invalid_fragments`. Original row indices were preserved.

The notebook inspected the beginning and end of the linker column and confirmed that a cell contained a Python list. It also checked the retained lists for the exact strings `[Zn][Zn]`, `[Cu][Cu]`, and `[O]`; zero rows contained these exact unwanted fragments.

---

## 11. Descriptor smoke test and saved outputs

The first extracted linker was:

```text
O=C([O-])c1ccc(C(=O)[O-])cc1
```

An exploratory descriptor function produced molecular weight 164.116, TPSA 80.26, HBD 0, HBA 4, rotatable bonds 2, ring count 1, formal charge −2, and aromatic fraction 0.5. The aromatic fraction in this function is aromatic atom count divided by heavy-atom count. This was a single-linker demonstration, not evidence that these extra features were calculated across the whole dataset.

The notebook contains save commands for:

```python
data/processed/hmof_linker_extracted.csv
data/processed/hmof_linker_extracted.pkl
```

Pickle preserves the list-valued columns. CSV serializes those lists as text and requires conversion when they are loaded again for list operations.

The excluded rows and error information were collected in notebook variables, but no separate export of the exclusion audit is shown. A reproducibility follow-up is to save that audit with `filename`, original index, reason, chemical representation, invalid fragments, and complete error messages.

---

## 12. Boundaries of the completed validation

The completed workflow establishes that every retained row has at least one fragment accepted by the implemented rules and RDKit sanitization. The following are not established by the saved checks:

- That every retained fragment is a framework-bridging organic linker. The function contains no explicit carbon-presence or connectivity-role requirement.
- That all retained fragments are metal-free. Single metal atoms and two exact metal dimers are filtered, but there is no general metal-containing-fragment rejection.
- That every candidate fragment in a retained MOF succeeded. A row can contain both retained linkers and `invalid_fragments`; the number of such partially successful rows is not reported.
- That linker multiplicities were preserved as stoichiometric information or standardized as unique types. The extraction function appends fragments without sorting or deduplicating them.
- That ambiguity has been quantified separately. The notebook distinguishes complete failures and zero-linker rows, but does not report a separate ambiguity count.

These boundaries describe the method actually used and should remain visible when interpreting later modeling results.

---

## 13. Handoff to descriptor generation

This notebook ends with the 25,929-row, 14-column linker-extracted dataset. In subsequent work reported in the project conversation, linker lists were expanded to `linker_1` through `linker_13`, and 15 selected descriptors per position were added. That later dataset has 195 descriptor columns and 222 total columns.

The 222-column result is a later stage, not the saved extraction output demonstrated in this notebook. The current modeling objective is to compare geometry-only and geometry-plus-linker-chemistry models on the same final retained rows and identical splits.

---

## Notebook evidence map

| Topic | Source cell positions |
| --- | --- |
| Input, duplicates, placeholder removal | 2–8 |
| `ERROR` subset and complete parsing diagnostics | 9–26 |
| Chemical representation and disconnection example | 27–31 |
| Final extraction function and batch application | 32–34 |
| Exclusion classification and identifiers | 35–40 |
| Retained dataset and exact-fragment check | 41–43 |
| Single-linker descriptor demonstration | 44–47 |
| CSV and pickle save commands | 48–49 |

---

