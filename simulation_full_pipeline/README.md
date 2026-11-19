# Notebook 6: simulation of the full PE3 pipeline

Simulation study for protocol v0.5.1 (ChroniCare-AI), written in response to Dr. Gaur's review of the primary test. It continues notebooks 1 to 5 of the [VitalDB rehearsal](../chronicare-prisma-recovery/vitaldb_rehearsal/README.md).

**Everything here is simulated. No real data of any kind is used** (`"datos_reales": "ninguno (todo simulado)"` in `sim6_parametros.json`). The data-generating model (measurement noise, sampling pattern, shape of recovery) rests on **assumptions** taken from the VitalDB rehearsal. Definitive numbers must be recomputed with the real noise, measurement frequency and coupling once the hospital data dictionary is available. Nothing in this folder is a result about the Biological State Hypothesis.

The notebook text and the code comments are in English (translated on 19 November 2026 from the Spanish originals, which are kept unchanged in the `archive_original_runs/` folder). File names, variable names and CSV column names remain in Spanish so that the published files and their fingerprints stay valid; see the glossary below. The translation changed no formula, seed or logic: after removing comments, docstrings and printed text, the abstract syntax trees of the English and Spanish code are identical, and `fullsim.py` and `fullsim2.py` give identical arrays for the same seed.

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
| `Notebook6_full_pipeline_simulation.ipynb` | English version of the notebook, without saved outputs. Run it in Google Colab. |
| `fullsim.py` | The simulator and the analysis, written by the notebook (step 1). |
| `requirements_sim6.txt` | Pinned library versions of the run. |
| `sim6_parametros.json` | Seed, grids, repetitions, library versions. |
| `sim6_huellas.json` | First 16 hex characters of the SHA-256 of each output file. Only the entry for `fullsim.py` differs from the original (`archive_original_runs/sim6_huellas.json`), because its comments were translated; the output files are the same. |
| `Notebook7_reproduce_simulation7.ipynb` | English notebook that re-runs Simulation 7 from scratch and compares the results with the published `sim7_*.csv` files (see the last section). |
| `archive_original_runs/` | Unmodified records of the original runs, kept as evidence: the original Spanish notebook, scripts and fingerprints, and the researcher's Colab reproduction of Simulation 7. It has its own README. |
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

## Glossary of Spanish names (CSV columns and parameters)
`resultado` = outcome (R, F or Rb, see above); `n` = number of eligible patients; `ruido` = measurement noise; `c` = coupling; `efecto_por_SD` = reference linear effect per SD of baseline BSI; `pendiente_nula_media` = mean slope in the null world (the bias produced by coupling and noise); `p95` = 95th percentile of the null slope; `elegibles_media` = mean number of eligible events; `valor_critico` / `valor_critico_acotado` = critical value (whole grid / restricted grid); `celda_que_manda` = grid cell that sets the critical value; `error_MC` = Monte Carlo error; `tamano_calibrado` / `tamano_sin_calibrar` = test size with / without the calibrated critical value; `poder_calibrado` = calibrated power; `pendiente_media_observada` = mean observed slope; `delta_ref` = reference effect in outcome units; `semiancho_IC` = half-width of the confidence interval; `criterio_i_poder` / `criterio_ii_precision` / `suficiente` = sufficiency criteria (i) power and (ii) precision, and whether both are met; `peor` / `mediana` / `mejor` = worst / median / best cell; `celdas_suficientes` = number of the 12 cells meeting both criteria; `peor_con_efecto_0_05` = worst power at effect 0.05; `techo` = ceiling strength; `poder_techo_dbeta` = power of the ceiling contrast Δβ; `poder_prueba_promedio` = power of the average test; `semilla` = seed; `reps` = repetitions; `acoplamientos` = coupling values; `ruidos` = noise values.

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

## Simulation 7 (protocol v0.6, one-sided alpha 0.025)

Same generator and seeds as Notebook 6 (`fullsim2.py` only adds outputs; with the 95th percentile it reproduces the Notebook 6 critical values). Added: one-sided alpha 0.025 (97.5th percentile), sensitivity (7), several D_min thresholds for F, and the ceiling contrast for F. All data are simulated.

| File | Content |
|---|---|
| `fullsim2.py`, `run_sim7.py`, `analizar7.py` | simulator, runner (about 30 min on 2 cores), analysis |
| `sim7_valores_criticos.csv` | critical values at alpha 0.05 and 0.025 |
| `sim7_tamano.csv`, `sim7_poder_suficiencia.csv` | size, power and sufficiency per cell |
| `sim7_sensibilidad7_regla.csv` | sensitivity (7) null slope and the registered decision rule |
| `sim7_Dmin_F.csv` | F with D_min = 0.1, 0.25, 0.5, 1.0 |
| `sim7_techo_dbeta.csv` | ceiling contrast for R and F |

Main findings: sufficiency at N=738 is unchanged (R 4/12 cells, F 8/12); the sign of sensitivity (7) does not discriminate (its null slope is positive in 100% of null replicates); the ceiling contrast does not reach 0.80 for a moderate ceiling for R or F. The generator applies the ceiling to the recoverable fraction, which favours F.

## Independent reproduction of Simulation 7 (19 November 2026)

The researcher re-ran Simulation 7 in full in Google Colab (Python 3.13, numpy 2.4.6, 2 cores, 2 h 47 min) with `Notebook7_reproduce_simulation7.ipynb`, using the repository code at commit `6904c12`; the executed notebook is saved as `Notebook7_executed_colab_2026-11-19.ipynb` (its printed headers are in Spanish because it ran the original Spanish scripts). Five of the six output files (`sim7_valores_criticos.csv`, `sim7_tamano.csv`, `sim7_poder_suficiencia.csv`, `sim7_sensibilidad7_regla.csv`, `sim7_Dmin_F.csv`) were identical to the published ones (maximum difference about 1e-16). The sixth, `sim7_techo_dbeta.csv` (ceiling contrast, exploratory), differed slightly: maximum difference 0.013 in power (4 of 300 replicates); the maximum power of the ceiling contrast for the R-based AC was 0.050 with 738 patients and 0.057 with 5,000, against 0.050 and 0.060 in the original run. The probable cause is a platform-dependent numerical difference in the quantile-regression fit (not verified). No conclusion changes.
