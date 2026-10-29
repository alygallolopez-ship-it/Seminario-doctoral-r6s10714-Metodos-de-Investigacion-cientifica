# Doctoral Seminar R6S10714 — Research Methods (Dr. Loveleen Gaur)

**Student:** Aly Gallo López · PhD in Deep Tech, FISI-UNMSM

This repository is the cumulative record of my work for Classes 1–7. The doctoral project is **ChroniCare-AI**: a multimodal-temporal Biological State Index (BSI) built from hospital electronic health records, used to test whether biological state constrains *Adaptive Capacity*, defined as recovery after a physiological perturbation (the Biological State Hypothesis). The project follows the Design Science Research paradigm. Each row below links the evidence for one class and states honestly what is complete and what is still pending. Nothing here contains patient data or data under a data-use agreement.

## Index by class

| Class | Topic | Evidence | Status |
|---|---|---|---|
| 1 | Research idea and paradigm (Design Science Research) | [entregable1_final_EN.docx](entregable1_final_EN.docx) | Complete |
| 2 | Method-fit matrix (weighted criteria, elimination rule) | [entregable2_final_EN.docx](entregable2_final_EN.docx) | Complete |
| 3 | Research protocol (10 components) | **Current: [protocolo_v0.4.docx](protocolo_v0.4.docx)**. History: [protocolo_v0.3_EN.docx](protocolo_v0.3_EN.docx), [protocolo_FINAL.docx](protocolo_FINAL.docx), [addendum_v3_EN.docx](addendum_v3_EN.docx), [addendum_FINAL_EN.docx](addendum_FINAL_EN.docx) | v0.4 complete; registration pending (see below) |
| 3 | Pre-data null simulation for the primary test (supports protocol §6.4.7) | [BSI_simulacion_nula_PE3_v2_completa.ipynb](BSI_simulacion_nula_PE3_v2_completa.ipynb) (full pipeline, executed, results saved in the notebook) | Complete; provisional until real sampling and noise are known |
| 3 | Rehearsal of the protocol on real public data (VitalDB, open dataset, CC BY 4.0): feasibility, measurement noise, coupling and power | Notebooks 01 to 05 in [chronicare-prisma-recovery/vitaldb_rehearsal](chronicare-prisma-recovery/vitaldb_rehearsal) | Exploratory. Shows the primary test needs far more patients with two pre-operative draws than VitalDB offers; the choice of primary test is pending with Dr. Gaur |
| 4 | Systematic review (PRISMA 2020), **current version v2**: recovery after a perturbation, PubMed + Scopus, 12 included studies | Start at [chronicare-prisma-recovery/README.md](chronicare-prisma-recovery/README.md). Report and PRISMA diagram: [Deliverable4_v2.docx](chronicare-prisma-recovery/deliverable4_v2/Deliverable4_v2.docx), [PRISMA_2020_flow_v2.png](chronicare-prisma-recovery/deliverable4_v2/PRISMA_2020_flow_v2.png). Screening: [PubMed](chronicare-prisma-recovery/screening/Screening_PubMed_125.xlsx), [Scopus](chronicare-prisma-recovery/screening/Screening_Scopus_103.xlsx). Extraction: [12 studies](chronicare-prisma-recovery/extraction/Extraction_12_included_studies.xlsx). Risk of bias: [QUIPS draft](chronicare-prisma-recovery/risk_of_bias/QUIPS_draft_12_studies.xlsx) | v2 complete (single reviewer; QUIPS is a draft). Not registered |
| 4 | Systematic review **v1, superseded** (old objective: adverse-event prediction, Scopus only) | [Entregable4_EN.docx](Entregable4_EN.docx), [Cribado_Scopus_174.xlsx](Cribado_Scopus_174.xlsx) (copies also in [archive_superseded](chronicare-prisma-recovery/archive_superseded/v1)) | Kept as history; replaced by v2 because the project objective changed |
| 5 | Reproducible ML pipeline | Separate repository: [Chronicare-ml-pipeline](https://github.com/alygallolopez-ship-it/Chronicare-ml-pipeline) (code, tests, per-seed results) | Complete |
| 6 | Reproducibility audit (Biolearn) | [Git_audit_Biolearn_Aly_FINAL.ipynb](Git_audit_Biolearn_Aly_FINAL.ipynb) | Complete |
| 7 | Baselines, seeds, ablation, Model Card, Datasheet, scorecard | [BSI_NHANES_ejercicios_1a6_ModelCard_Datasheet.ipynb](BSI_NHANES_ejercicios_1a6_ModelCard_Datasheet.ipynb), [MODEL_CARD.md](MODEL_CARD.md), [DATASHEET.md](DATASHEET.md) | Complete for NHANES; exploratory (see below) |

## Supporting analyses (evidence behind Class 7 and protocol §4)

- [BSI_NHANES_v4_1_tiempo_hasta_evento.ipynb](BSI_NHANES_v4_1_tiempo_hasta_evento.ipynb): the primary NHANES analysis (public CDC data, downloaded by the notebook). Written in Spanish.
- [BSI_NHANES_valor_anadido_v3.ipynb](BSI_NHANES_valor_anadido_v3.ipynb): earlier version of the NHANES analysis (binary outcome, logistic model, AUC; no time-to-event and no survey weights). Kept as history; v4.1 is the version cited in the protocol and the Model Card. Written in Spanish.
- [BSI_MIDUS3_respuesta_al_reto.ipynb](BSI_MIDUS3_respuesta_al_reto.ipynb): the MIDUS 3 evaluation. **It contains no data**: MIDUS is under an ICPSR data-use agreement and cannot be redistributed. Written in Spanish.

## What is *not* done (stated on purpose)

- **Adaptive Capacity (PE3) has not been tested.** The NHANES and MIDUS analyses are cross-sectional or single-challenge and cannot test it; they are exploratory evidence about the BSI only.
- **The BSI added a small gain in NHANES** (ΔC +0.007, 95% CI 0.003 to 0.011) that did **not** exceed the same markers used as continuous variables, and it added nothing in MIDUS. Reported as findings, not hidden.
- **Exercises 1–3 are exploratory**, run after the primary analysis was fixed and on the same data. The domain ablation is post hoc and does not change the BSI definition.
- **Not assessed:** calibration, net benefit, external validation. Licence and DOI of this repository: UNKNOWN (Zenodo planned).
- **Sample-size numbers for PE3 are provisional**, from a parametric simulation with assumed noise.
- **Pending decisions and registration:** protocol v0.5 is **not written yet**; it waits for the decision with Dr. Gaur on the primary test (ceiling contrast vs mean-level association, based on the VitalDB rehearsal). OSF pre-registration comes after that (and after the empirical simulation); UNMSM ethics committee (not yet open for filing); data access from the hospital (in process).
- **Systematic review v2:** one reviewer, one pass; the risk-of-bias table is a draft without a second reviewer. The VitalDB numbers are a rehearsal with assumed noise and an approximate coupling estimate, not results about the hypothesis.

## How to reproduce

- NHANES notebooks: open in Google Colab and choose *Runtime → Run all*. No upload is needed; all data are downloaded from the CDC.
- Simulation notebook: open in Colab; for a quick test set `REPS=30, BOOT=10`; the full run (150 repetitions) takes about 20-25 minutes.
- VitalDB rehearsal notebooks (folder above): saved without outputs; open in Colab and choose *Runtime → Run all*. The data are the public VitalDB open dataset and are not stored in this repository.
- Systematic review v2: the screening and extraction tables are the record of every decision; the PRISMA counts in the diagram match the screening sheets.
- MIDUS: requires obtaining the data from ICPSR under its data-use agreement.