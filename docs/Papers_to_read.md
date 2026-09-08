# MOF Project — Papers to Read

## Purpose

Track the key literature that will guide the upgrade of the CO₂ adsorption project from descriptor-based machine learning toward chemistry-aware models, advanced MOF representations, GNNs, Transformers, and LLM-assisted workflows.

---

## Reading List

| # | Paper | Technology / Focus | Why Read It | Stage |
|---|---|---|---|---|
| 1 | **Engineering Machine-Learning Features for CO₂/N₂ Adsorption (2024)** — Deng & Sarkisov | Descriptor / Feature Engineering | Closest to the current project. Understand what information can be added beyond LCD, PLD, void fraction, and surface area. | **READ FIRST** |
| 2 | **Transformer-based Gas Adsorption Prediction in MOFs (2024)** — Wang et al. | Transformer / MOF Representation | Learn how Transformer-based representations can be used for gas-adsorption prediction. | **NEXT** |
| 3 | **MMAGNN: Multimodal Graph Neural Network for CO₂ Adsorption (2025)** | GNN / 3D Structure / Attention | Understand how atomic graphs, 3D coordinates, and attention can improve CO₂ prediction and interpretation. | **GNN PHASE** |
| 4 | **MCLFormer: CO₂ Adsorption Prediction Using hMOF (2026)** | CNN / LSTM / Transformer / MOFid | High-priority comparison because it uses hMOF and is directly relevant to the current dataset and CO₂ target. | **HIGH PRIORITY** |
| 5 | **SpbNet: Foundation Model for Porous Materials (2026)** | Foundation Model / Pretrained Representation | Learn how pretrained representations and foundation models are being applied to porous materials and hMOF-related tasks. | **ADVANCED** |
| 6 | **MOFMeld: MOF Structural Embeddings + Specialized LLM (2026)** | LLM / Embeddings / Knowledge Grounding | Read last. Understand how an LLM can be integrated with structural representations and scientific knowledge. | **LLM PHASE** |

---

## Paper Links

### 1. Engineering Machine-Learning Features for CO₂/N₂ Adsorption

https://doi.org/10.1021/acs.jpcc.4c01692

### 2. Transformer-based Gas Adsorption Prediction in MOFs

https://www.nature.com/articles/s41467-024-46276-x

### 3. MMAGNN: Multimodal Graph Neural Network for CO₂ Adsorption

https://www.nature.com/articles/s42005-025-02399-1

### 4. MCLFormer: CO₂ Adsorption Prediction Using hMOF

https://doi.org/10.1016/j.commatsci.2026.114864

### 5. SpbNet: Foundation Model for Porous Materials

https://www.nature.com/articles/s41467-026-69245-y

### 6. MOFMeld: MOF Structural Embeddings + Specialized LLM

https://doi.org/10.1038/s44387-026-00106-1

---

## Reading Strategy

Do not read all papers at once.

Start with **Paper 1**.

For each paper, record:

- Dataset
- Input features / MOF representation
- Model
- Prediction target
- Pressure(s)
- Performance metrics
- Explainability method
- Main contribution
- Limitations
- What can be adapted to this MOF project

---

## Reading Progress

- [ ] Paper 1 — Engineering ML Features
- [ ] Paper 2 — Transformer-based Gas Adsorption Prediction
- [ ] Paper 3 — MMAGNN
- [ ] Paper 4 — MCLFormer
- [ ] Paper 5 — SpbNet
- [ ] Paper 6 — MOFMeld

---

## Project Question to Keep in Mind

> **How does increasing the richness of MOF representation — from simple physical descriptors to chemical descriptors and learned representations — change CO₂ adsorption prediction and interpretation across pressure regimes?**