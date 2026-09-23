# Linker Descriptors and CO₂ Uptake: XGBoost Interpretation

## 1. Objective and Data

This analysis asks whether descriptors of organic linkers add predictive information beyond four pore-geometry descriptors for simulated CO₂ uptake in hypothetical metal–organic frameworks (MOFs).

The chemistry dataset contains 25,928 MOFs. Separate XGBoost regressors predict uptake at 0.01, 0.05, 0.1, 0.5, and 2.5 bar. For each pressure, two models use the same train, validation, and test rows:

| Model | Inputs |
|---|---|
| Structural | LCD, PLD, void fraction, and gravimetric surface area |
| Structural + linker | The four structural descriptors plus 195 RDKit descriptors: 15 properties for each of up to 13 extracted linker positions |

The models used 200 trees, learning rate 0.1, maximum depth 3, and minimum child weight 1. These settings were selected at 0.01 bar and reused at the other pressures. SHAP values were calculated for the same sample of 200 validation rows at every pressure. The plots of mean absolute SHAP values rank the magnitude of feature contributions to predictions; they do not show whether higher feature values increase or decrease uptake.

## 2. Predictive Contribution of Linker Descriptors

Adding linker descriptors improved performance on the held-out test split at every pressure.

| Pressure (bar) | Structural MAE (mol/kg) | Structural + linker MAE (mol/kg) | MAE reduction | Structural R² | Structural + linker R² |
|---:|---:|---:|---:|---:|---:|
| 0.01 | 0.0750 | 0.0611 | 18.6% | 0.4521 | 0.6174 |
| 0.05 | 0.2063 | 0.1518 | 26.4% | 0.5631 | 0.7530 |
| 0.1 | 0.3069 | 0.2164 | 29.5% | 0.5939 | 0.7870 |
| 0.5 | 0.6702 | 0.4323 | 35.5% | 0.6117 | 0.8367 |
| 2.5 | 1.1584 | 0.7416 | 36.0% | 0.6355 | 0.8532 |

The test improvements are consistent with the validation results. They show that the set of added linker descriptors provides predictive information on this row-based split. The increasing percentage reduction in MAE with pressure does not support a claim that linker effects are strongest at low pressure.

## 3. What the SHAP Rankings Show

In the model containing structural and linker descriptors, individual structural columns generally rank above individual linker columns. Surface area leads the displayed rankings at 0.01–0.5 bar; PLD leads at 2.5 bar. Void fraction also ranks highly throughout. This is a change in model attribution, not direct proof of a transition between adsorption mechanisms.

Several linker columns appear repeatedly in the displayed top-feature rankings:

| Descriptor family | Examples in the displayed rankings | Careful interpretation |
|---|---|---|
| Partial charge | `MinPartialCharge`, `MaxPartialCharge` | The model uses computed charge extrema; the ranking alone does not locate a CO₂ binding site or establish an electrostatic mechanism. |
| Ring and carbon character | `NumAromaticRings`, `FractionCSP3` | These features represent aspects of linker composition and shape; neither is a direct measure of CO₂–π binding or framework flexibility. |
| Size and polarity | `MolWt`, `TPSA`, `LogP`, `LabuteASA` | These can correlate with multiple chemical and geometric properties. Their SHAP magnitudes do not establish a favorable direction of effect. |
| Conformational proxy | `RotatableBonds` | A count of bonds that can rotate in an isolated linker does not measure flexibility in the assembled framework. |

The plot lists only the top individual columns. A linker property spread over positions linker_1 to linker_13 may have a larger collective contribution than any one position suggests. Conversely, summing mean absolute SHAP values across correlated positions should be described as an attribution summary, not as a unique physical effect.

The earlier draft listed specific SHAP magnitudes, including surface-area importance of 0.1376 and linker_1_MinPartialCharge importance of 0.0143. Those values should be included only after confirming the exact pressure, fitted model, and sample from the underlying importance table. The five-panel figure alone does not establish them as cross-pressure values.

## 4. Limits on Chemical Interpretation

Direction is unknown from mean absolute SHAP. Beeswarm or dependence plots are needed to examine whether higher descriptor values are associated with higher or lower predictions, including possible interactions.

Feature positions are ordered labels. linker_1 is not a consistent chemical role across MOFs. Later linker slots are absent for many rows, and their missingness or the number of linkers may itself carry information.

Structural descriptors are correlated. Surface area, void fraction, LCD, and PLD may share attribution. Linker properties may also correlate with them.

The adsorption mechanism is not directly measured. These models do not report binding energies, site-resolved interactions, isosteric heats, or whether 2.5 bar is near saturation. Terms such as Henry’s-law regime, quadrupole–π binding, and pore filling require additional evidence for this dataset.

Split sensitivity remains to be checked. The current split is row-based, while some MOFIDs repeat. A follow-up evaluation that keeps related structures in the same split would help assess generalization to unseen frameworks.

## 5. Next Analyses

- Group the 13 positions for each of the 15 linker descriptor types and plot their aggregate SHAP at each pressure. Report clearly how the group attribution is calculated.

- Use beeswarm and dependence plots for leading descriptors to examine direction and interactions, including missing-value patterns.

- Compare the distributions and uptake ranges at each pressure before interpreting differences in absolute SHAP magnitude.

- Repeat the performance comparison with a split that keeps repeated MOFIDs together, then compare it with the current row-based result.

## 6. Conclusion

On the held-out test split, adding RDKit linker descriptors to four pore-geometry features reduced CO₂ uptake prediction MAE by 18.6–36.0% across five pressures. Thus, the linker representation adds substantial predictive information beyond the selected geometry descriptors.

Test R² also rises at every pressure. Structural columns remain the largest individual SHAP contributors in the displayed rankings, with PLD becoming the top displayed feature at 2.5 bar. Specific linker mechanisms and a pressure-driven switch from chemistry control to structural control remain hypotheses for further analys.