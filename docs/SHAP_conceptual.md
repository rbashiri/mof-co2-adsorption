2. What is SHAP?

SHAP = SHapley Additive exPlanations.
In simple terms, SHAP examines a prediction and asks:
How much did each feature contribute to moving this prediction higher or lower?
Global SHAP = understand the entire dataset/model.
Local SHAP = understand one individual MOF prediction.

`R² tells me how well the four features collectively predict CO₂ uptake. SHAP tells me how individual features contribute to those predictions.`
Example 

| Feature       | SHAP value |
| ------------- | ---------: |
| Surface area  |       +0.7 |
| Void fraction |       +0.3 |
| LCD           |       −0.2 |
| PLD           |       +0.1 |

`SHAP >0 ⇒ pushes prediction upward`
`SHAP<0 ⇒ pushes prediction downward​`
And the magnitude tells us the strength of that contribution:
+0.7 has a stronger contribution than +0.1.
a positive SHAP value does not mean that a feature is always positively related to CO₂ uptake. It means that for that observation, given the model and other features, the feature pushed the prediction upward.

`SHAP sign = direction of contribution.`
`SHAP magnitude = strength of contribution.`

### SHAP summary plot (beeswarm plot)
The beeswarm plot is designed to display an information-dense summary of how the top features in a dataset impact the model’s output.
What does a SHAP beeswarm answer?

It combines three questions:

Which feature is most important?
Does it push predicted CO₂ uptake higher or lower?
Do high or low values of that feature cause that behavior?
                    SHAP value
                ← lower   0   higher →

Surface area      • • • • | • • • • •
Void fraction       • • • | • • •
PLD                    • • | • •
LCD                     •  | •

The features on the Y-axis are usually ordered by overall importance. If surface_area_m2g is at the top, it means it has the largest average SHAP magnitude across the analyzed MOFs.

The X-axis is the SHAP value:

Left of zero → pushes predicted CO₂ uptake down
Right of zero → pushes predicted CO₂ uptake up
Farther from zero → stronger contribution.
But there is one more piece: color.

Typically:

Red = high actual feature value
Blue = low actual feature value
Y-axis = feature importance/order
X-axis = direction and magnitude of contribution
Color = whether the original feature value is high or low

``` Python
import shap
# 1. Create an explainer for the trained model
explainer = shap.Explainer(model, X_train)

# 2. Calculate SHAP values for the data you want to explain
shap_values = explainer(X_test)

# 3. Global explanation — feature importance + direction
shap.plots.beeswarm(shap_values)

# 4. Global feature importance only
shap.plots.bar(shap_values)

# 5. Explain one individual prediction
shap.plots.waterfall(shap_values[0])

# 6. Examine the effect of one feature
shap.plots.scatter(shap_values[:, "feature_name"])
```
