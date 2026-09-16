
# Phase 2 — MOFID Chemistry Preparation

## Created the Chemistry Subset

- Started from the cleaned Phase 1 dataset.
- Selected the 27,706 records with non-null MOFID information.

## Assessed MOFID Quality

- Identified placeholder representations such as `MOFid-v1.NA.NA` and
	`MOFid-v1.NA.NAno_mof`.
- Removed 1,754 NA-type records.
- The final dataset for further chemistry analysis contains **25,952 MOFs**.

## Tested Complete MOFID Chemical Representations with RDKit

- Extracted the chemical portion before the MOFID metadata.
- Tested whether RDKit could parse each complete chemical representation.

| RDKit parsing result | Number of MOFs |
| --- | ---: |
| Parsed successfully | 12,940 |
| Failed standard RDKit parsing | 13,012 |

## Investigated the Failed Records

- Examined common patterns instead of immediately removing failed records.
- Found that 12,284 of the 13,012 failures contain the specific Zn–O fragment:

	```text
	[Zn][O]([Zn])([Zn])[Zn]
	```

- Only 63 failures were labeled `ERROR`.
- Only 6 failures contained `N#N`.

These results suggest that complete-MOF parsing failure is primarily associated
with how some metal and coordination fragments are represented, rather than
simply with invalid MOFID records.

## Tested Fragmentation

- Split representative chemical strings using `.` into disconnected
	components.
- Found that an organic linker fragment can parse successfully even when the
	complete MOF representation fails.
- Observed that **fragment order is not reliable**: metal-containing fragments
	can occur in different positions.

### Current Conclusion

The next task is therefore **not to discard the 13,012 failed MOFs**. Instead,
the complete set of **25,952 MOFIDs** should be fragmented and systematically
characterized so that organic linker fragments can be identified independently
of their position and analyzed with RDKit.