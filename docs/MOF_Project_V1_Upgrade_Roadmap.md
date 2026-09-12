# MOF Project V1 — Upgrade Roadmap

**Target Completion: December 31, 2026**

## Roadmap
```
| Phase | Upgrade | Main Goal | Deadline |
|---|---|---|---|
| 1 | Baseline + Explainability | RF all pressures + SHAP | Sep 19 |
| 2 | Chemistry-Aware ML | Add chemical descriptors | Oct 17 |
| 3 | MOF Representations | MOF-specific descriptors | Nov 7 |
| 4 | Deep Learning | GNN model | Nov 21 |
| 5 | Transformer / Embeddings | Pretrained representations | Dec 5 |
| 6 | LLM + RAG | Literature + model explanations | Dec 19 |
| 7 | Final System | Integration + documentation | Dec 31 |
```
## Progress

- [ ] Phase 1 — Baseline + Explainability
- [ ] Phase 2 — Chemistry-Aware ML
- [ ] Phase 3 — MOF Representations
- [ ] Phase 4 — Deep Learning
- [ ] Phase 5 — Transformer / Embeddings
- [ ] Phase 6 — LLM + RAG
- [ ] Phase 7 — Final System
```text 
# MOF Project Upgrade Roadmap

## Scientific Progression

The project will progressively move from simple, physically interpretable structural descriptors toward chemistry-aware, structure-based, and learned MOF representations.

**Geometry → Chemistry → CIF / Pore Structure → Learned Representation → Scientific AI System**

---

## Roadmap
| Phase | Scientific Step                | Upgrade                          | Main Goal                                                                                       | Deadline |
| ----- | ------------------------------ | -------------------------------- | ----------------------------------------------------------------------------------------------- | -------- |
| **1** | **Geometry**                   | Baseline + Explainability        | 4 structural features → Random Forest at all pressures → SHAP → scientific interpretation       | Sep 19   |
| **2** | **Chemistry**                  | Chemistry-Aware ML + RDKit       | Learn RDKit → extract chemical/linker descriptors → combine chemistry with geometric features   | Oct 17   |
| **3** | **CIF / Pore Structure**       | MOF-Specific Descriptors + Zeo++ | CIF → Zeo++ → extract additional pore/geometric descriptors → improve structural representation | Nov 7    |
| **4** | **Learn Representation**       | Transformer Foundations          | Learn PyTorch → embeddings → attention → self-attention → build a simple Transformer            | Nov 21   |
| **5** | **Learned MOF Representation** | Pretrained MOF Transformer       | CIF → pretrained MOF Transformer → extract learned MOF embeddings/representations               | Dec 5    |
| **6** | **Compare & Integrate**        | Representation Comparison        | Compare geometry vs. chemistry vs. Zeo++ descriptors vs. Transformer representations            | Dec 12   |
| **7** | **Scientific AI**              | LLM + RAG                        | Connect model predictions and SHAP results with scientific literature and explanations          | Dec 19   |
| **8** | **Complete System**            | Final Integration                | Integrate the pipeline → testing → documentation → final system                                 | Dec 31   |


## Research Progression
### Phase 1 — Geometry

```text
LCD + PLD + Void Fraction + Surface Area
                    ↓
              Random Forest
                    ↓
              CO₂ Uptake
                    ↓
                  SHAP
                    ↓
        Scientific Interpretation
```

**Question:** How much of CO₂ adsorption behavior can be explained using a small set of physically meaningful geometric descriptors?

---

### Phase 2 — Chemistry

```text
MOF Chemical Information
          ↓
        RDKit
          ↓
Chemical / Linker Descriptors
          +
Geometric Descriptors
          ↓
     Random Forest
          ↓
      CO₂ Uptake
```

**Question:** How much predictive information does MOF chemistry add beyond pore geometry?

---

### Phase 3 — CIF / Pore Structure

```text
CIF Structure
     ↓
   Zeo++
     ↓
MOF-Specific Pore Descriptors
     ↓
Geometry + Chemistry + CIF-Derived Features
     ↓
              ML Model
```

**Question:** Can additional descriptors extracted directly from MOF structures improve adsorption prediction?

---

### Phase 4 — Transformer Foundations

Learn the concepts required to understand and use Transformer models:

```text
PyTorch
   ↓
Tensors + Neural Networks
   ↓
Embeddings
   ↓
Attention
   ↓
Self-Attention
   ↓
Simple Transformer
```

---

### Phase 5 — MOF Transformer

```text
CIF Structure
     ↓
Pretrained MOF Transformer
     ↓
Learned MOF Representation
     ↓
Transformer Embeddings
     ↓
CO₂ Adsorption Prediction
```

**Question:** What structural and chemical information can a pretrained Transformer learn that is not explicitly captured by engineered descriptors?

---

### Phase 6 — Model and Representation Comparison

Compare progressively richer representations:

```text
Model A
Geometry
↓
RF

Model B
Geometry + Chemistry
↓
RF

Model C
Geometry + Chemistry + Zeo++ Features
↓
RF

Model D
Transformer Representation
↓
Prediction

Model E
Engineered Features + Transformer Embeddings
↓
Prediction
```

Evaluate each approach using:

* MAE
* RMSE
* R²
* SHAP / interpretability
* Generalization performance

---

## Central Research Question

> **How does progressively adding geometric, chemical, CIF-derived, and Transformer-learned representations improve the prediction and scientific understanding of CO₂ adsorption in metal-organic frameworks?**

---

## Final Vision

```text
Geometry
   ↓
Chemistry
   ↓
CIF / Pore Structure
   ↓
Transformer Representation
   ↓
Prediction + Explainability
   ↓
Scientific Literature (RAG)
   ↓
Integrated MOF Scientific AI System
```

``` 
```


