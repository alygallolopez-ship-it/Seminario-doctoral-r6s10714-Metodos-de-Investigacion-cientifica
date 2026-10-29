# ChroniCare-AI: systematic review of recovery after acute physiological perturbation

Author: Aly Gallo · Seminario Doctoral (R6S10714), Doctorado en Deep Tech, FISI-UNMSM · Advisor: Dr. Loveleen Gaur

## What this repository contains
| Folder | Content |
|---|---|
| `deliverable4_v2/` | Deliverable 4, version 2 (mini systematic review, PRISMA 2020 flow diagram, gap analysis) and the flow diagram as an image. |
| `screening/` | Record-by-record screening decisions: PubMed (125 records) and Scopus (103 unique records), searched 26 Oct 2026. |
| `extraction/` | Data-extraction sheet for the 12 included studies, plus a sheet listing the 3 studies removed from the earlier 15-row version (2 excluded at full text, 1 not retrievable). Every cell was checked against the full texts; changes and their sources are in the sheet "Control de cambios". Deliverable 4 v2 remains the authoritative version. |
| `risk_of_bias/` | Draft QUIPS ratings for the 12 included studies. Draft proposals for investigator review, not final decisions. |
| `vitaldb_rehearsal/` | Five Google Colab notebooks that rehearse the protocol on the open VitalDB dataset (feasibility, null simulation, measurement noise, coupling and power, mean-level test). Recovery is simulated; no real health outcome is analysed. |
| `archive_superseded/v1/` | Version 1 of Deliverable 4 (built for the previous objective) and its Scopus screening sheet (174 records). Kept unchanged as the record of the first Design Science Research cycle; do not cite. |

## Version history
- **v1** (early Oct 2026): objective was multimodal EHR prediction of adverse clinical events; Scopus only; 10 studies.
- **v2** (26 Oct 2026): objective is recovery after a defined acute perturbation as a measure of adaptive capacity; PubMed and Scopus; 12 included studies.

## Not included, on purpose
- Raw database exports (for example the Scopus CSV of version 1, which includes abstracts under Scopus terms of use).
- Full-text PDFs of the articles (copyright). The included studies are listed with DOIs in the Deliverable.
- Raw data. VitalDB data are downloaded by the notebooks from the VitalDB API (CC BY 4.0; Lee et al., Sci Data 2022, doi 10.13026/czw8-9p62 on PhysioNet).

## Reproducing the notebooks
Open each notebook in Google Colab and choose Runtime, then Run all. Seeds are fixed (2026). Library versions are printed at the start of each run; they are not yet pinned.

## Limits
Power figures in notebooks 02 to 05 come from simulations that assume shapes for the drop, the recovery and the ceiling. They are not clinical results.
