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

## Notes for readers who cross-check the files
- **Screening counts.** `screening/Screening_PubMed_125.xlsx` lists 13 included records and `Screening_Scopus_103.xlsx` lists 2 (15 in total). These are the counts **before full-text assessment**. After it, 2 reports were excluded and 1 could not be retrieved, leaving the **12** studies of the final review (see the sheet "Retirados tras revisión" in `extraction/Extraction_12_included_studies.xlsx`).
- **Figure in the Deliverable.** `deliverable4_v2/Deliverable4_v2.docx` still embeds the version-2 flow diagram (identical to `PRISMA_2020_flow_v2.png`). The current diagram (v3, which adds the duplicate-removal and screening-method steps) is the separate file `PRISMA_2020_flow_v3.pdf`. The counts are the same in both.
- **Residual duplicate.** After the 106 duplicates were removed, `screening/Screening_Scopus_103.xlsx` still holds two book chapters with the same DOI (10.1016/B978-0-12-809324-5.23592-X, EIDs 2-s2.0-85084710796 and 2-s2.0-85121858854). Both were excluded (R1), so the 12 included studies are unaffected, but the 228 screened records contain one duplicate. The matching key used for deduplication (DOI or title) was not recorded.
- **File names cited in the Deliverable.** The Deliverable cites working file names. In this repository they correspond to: `Cribado_PubMed_125_final.xlsx` = `screening/Screening_PubMed_125.xlsx`; `Cribado_Scopus_103.xlsx` = `screening/Screening_Scopus_103.xlsx`; `QUIPS_borrador_12.xlsx` = `risk_of_bias/QUIPS_draft_12_studies.xlsx`. Two cited files are **not yet in this repository**: `Revision_R3_R4.xlsx` and `Verificacion_ciega_20.xlsx` (the blind check of 20 exclusions).

## Version history
- **v1** (early Oct 2026): objective was multimodal EHR prediction of adverse clinical events; Scopus only; 10 studies.
- **v2** (26 Oct 2026): objective is recovery after a defined acute perturbation as a measure of adaptive capacity; PubMed and Scopus; 12 included studies.

## Not included, on purpose
- Raw database exports (for example the Scopus CSV of version 1, which includes abstracts under Scopus terms of use).
- Full-text PDFs of the articles (copyright). The included studies are listed with DOIs in the Deliverable.
- Raw data. VitalDB data are downloaded by the notebooks from the VitalDB API (CC BY 4.0; Lee et al., Sci Data 2022, doi 10.13026/czw8-9p62 on PhysioNet).

## Reproducing the notebooks
Open each notebook in Google Colab and choose Runtime, then Run all. Seeds are fixed (2026). Notebooks 01 to 05 are saved executed, with outputs (run of 17 Nov 2026), and their CSV tables, with SHA-256 fingerprints, are in `vitaldb_rehearsal/outputs/`. All library versions of that run are in `vitaldb_rehearsal/requirements_vitaldb.txt`. The numbers are identical to the earlier run of 27 Oct 2026. Details in `vitaldb_rehearsal/README.md`.

## Limits
Power figures in notebooks 02 to 05 come from simulations that assume shapes for the drop, the recovery and the ceiling. They are not clinical results.
