# Notebook 6: simulation of the full PE3 pipeline

Simulation study for protocol v0.5.1 (ChroniCare-AI), written in response to Dr. Gaur's review of the primary test. It continues notebooks 1 to 5 of the [VitalDB rehearsal](../chronicare-prisma-recovery/vitaldb_rehearsal/README.md).

**Everything here is simulated. No real data of any kind is used** (`"datos_reales": "ninguno (todo simulado)"` in `sim6_parametros.json`). The data-generating model (measurement noise, sampling pattern, shape of recovery) rests on **assumptions** taken from the VitalDB rehearsal. Definitive numbers must be recomputed with the real noise, measurement frequency and coupling once the hospital data dictionary is available. Nothing in this folder is a result about the Biological State Hypothesis.

The notebook and the comments in `fullsim.py` are written in Spanish; file and column names are in Spanish too.

## What the notebook does

It generates fake patients (the truth is known) and applies to them the whole PE3 analysis of the protocol:

1. robust nadir, then recovery R<sub>i</sub>;
2. expected recovery with patient-level cross-fitting (5 folds, without baseline BSI);
3. AC<sub>i</sub> = R<sub>i</sub> − expected recovery;
4. primary test: average slope β<sub>mean</sub> of AC on baseline BSI, one-sided, with patient-clustered standard errors.

The same pipeline is run on three outcomes: **R** (recovery, the primary outcome), **F** (fraction recovered, R/D) and **Rb** (R restricted to events with an observed drop > 0.5 SD, a sensitivity analysis). Simulated worlds: null, linear (+0.05 or +0.10 per SD of BSI) and ceiling (moderate 0.5, strong 1.0).

## Files

| File | What it is |
|---|---|
| `Cuaderno6_simulacion_pipeline_completo.ipynb` | The executed notebook (all code cells with outputs). Run it in Google Colab. |
| `fullsim.py` | The simulator and the analysis, written by the notebook (step 1). |
| `requirements_sim6.txt` | Pinned library versions of the run. |
| `sim6_parametros.json` | Seed, grids, repetitions, library versions. |
| `sim6_huellas.json` | First 16 hex characters of the SHA-256 of each output file. |
| `sim6_figura.png` | Summary figure. |
| `sim6_nulo_por_celda.csv` | Null slope, SD and 95th percentile for each grid cell. |
| `sim6_valores_criticos.csv` | Critical value per N: the largest 95th percentile over the whole grid, and which cell sets it. |
| `sim6_tamano_verificacion.csv` | Test size with the calibrated critical value, checked on independent repetitions (and without calibration). |
| `sim6_poder_suficiencia.csv` | Power per cell and effect size, with the two sufficiency criteria. |
| `sim6_resumen_por_n.csv` | Worst / median / best power over the grid for each N. |
| `sim6_malla_acotada.csv` | The same summary on the restricted grid. |
| `sim6_techo_dbeta.csv` | Power of the ceiling contrast (Δβ) and of the average test in the ceiling worlds. |

## Settings of the executed run (14 Nov 2026)

- Seed: `20261113`.
- Eligible patients N: 500, 738, 1000, 2000, 3000, 5000.
- Measurement noise: 0.15, 0.30, 0.60 (SD units of the BSI). Coupling: 0, 0.12, 0.24, 0.36.
- Repetitions: 2,000 for calibration, 1,000 independent for checking the test size, 1,000 for power, 300 for the ceiling contrast (grid: N 738/2000/5000, noise 0.15/0.30, coupling 0/0.36).
- Critical value for each N = the largest 95th percentile over the whole noise × coupling grid. The Monte Carlo error is reported next to each size and power.
- Sufficiency criteria: (i) calibrated power ≥ 0.80; (ii) half-width of the confidence interval ≤ the reference effect.
- Libraries: numpy 2.4.6, pandas 2.2.3, statsmodels 0.15.0, scipy 1.16.3, joblib 1.6.0, matplotlib 3.10.0 (as recorded in `sim6_parametros.json`).

## How to read the tables

Open `sim6_resumen_por_n.csv` and `sim6_poder_suficiencia.csv` together with `sim6_parametros.json`. The power depends strongly on the cell (noise, coupling, effect size), so a single figure per N hides the range: the summary file gives the worst, median and best cell, and `celdas_suficientes` counts how many of the 12 cells meet both criteria. Read the numbers as properties of the assumed generator, not as predictions for the hospital data.

## Reproducing

1. Open the notebook in Google Colab and choose *Runtime → Run all*. The full run is long (many thousands of repetitions, parallelized with joblib); a quick mode (`quick`) exists for testing and gives much smaller numbers of repetitions.
2. The seed is fixed, so the same libraries give the same tables.
3. To check the files of this folder, compare the first 16 characters of `sha256sum <file>` with `sim6_huellas.json`.

## Known limits

- All numbers come from assumed generator parameters; they are provisional until the hospital's noise, sampling pattern and coupling are known.
- The Monte Carlo error is not zero: compare differences between cells with the `error_MC` columns.
- The earlier null-simulation notebook in the repository root (`BSI_simulacion_nula_PE3_v2_completa.ipynb`) is the previous version of this work (simple slope on the recovered fraction, 150 repetitions). This folder supersedes it for the primary test.
