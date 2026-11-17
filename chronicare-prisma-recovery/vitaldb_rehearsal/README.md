# VitalDB rehearsal notebooks (01 to 05)

Five Google Colab notebooks that rehearse the protocol on the open VitalDB dataset. Recovery is simulated; no real health outcome is analysed. Raw data are not stored here: the notebooks download them from the VitalDB API (CC BY 4.0).

| Notebook | CSV tables (folder `outputs/`) |
|---|---|
| `01_feasibility.ipynb` | `conteo_por_prueba.csv`, `conteo_por_ventana.csv` |
| `02_null_simulation.ipynb` | `simulacion_nula_vitaldb.csv`, `simulacion_nula_control_n20000.csv` |
| `03_noise_and_methods.ipynb` | `sim3_comparacion_metodos.csv`, `sim3_control_n20000.csv` |
| `04_coupling_and_power.ipynb` | `sim4_poder_por_n.csv` |
| `05_mean_level_test.ipynb` | `sim5_poder_prueba_promedio.csv`, `sim5_n_minimo.csv` |

## Provenance of the notebooks and tables
- The five notebooks were run from start to finish in Google Colab on **17 Nov 2026** and are saved **with their outputs**. The analysis code is identical to the version of 27 Oct 2026. Two things were added: a note at the top ("Versión 2") and one final cell that records the library versions, computes the SHA-256 fingerprint of each CSV and packs the outputs.
- The nine CSV tables in `outputs/` are the files written by these notebooks in that run (not rebuilt by hand). `outputs/SHA256SUMS.txt` lists the full SHA-256 of each file; the first 16 characters match the fingerprints printed at the end of each notebook. To check: `cd outputs && sha256sum -c SHA256SUMS.txt`.
- `requirements_vitaldb.txt` records the versions of that run: Python 3.13.18, numpy 2.4.6, pandas 2.2.3, scipy 1.16.3, statsmodels 0.15.0, matplotlib 3.10.0.

## Comparison with the earlier run (27 Oct 2026)
The earlier run printed only Python 3.13.16, pandas 2.2.3 and numpy 2.1.3, and its CSV files were not kept. For that reason, the CSV tables first committed on 15 Nov 2026 (commit 5c60b51) had been rebuilt from the printed notebook outputs; the native files of the 17 Nov run are byte-for-byte identical to those rebuilt tables. Comparing the notebook outputs of the two runs, all printed tables are identical; only the date, the run times and some warning messages differ. So the results did not change with newer library versions (numpy 2.1.3 to 2.4.6), using the same fixed seeds (2026).

## Glossary of Spanish names (notebooks and CSV columns)
The notebooks are written in Spanish. Terms in the CSV tables: `ruido` = measurement noise (SD of the BSI); `acople` / `c` = coupling between baseline state and depth of fall; `metodo` = recovery-measure variant, defined in the notebook; `poder techo 0.5` / `1.0` = power to detect a moderate / strong ceiling; `poder efecto 0.05/SD` and `0.10/SD` = power for a linear effect of 0.05 / 0.10 per SD of baseline BSI; `n minimo` = smallest simulated N reaching power 0.80; `Δβ nulo, media` = mean ceiling contrast in the null world; `critico (p95)` = 95th percentile used as critical value; `pendiente nula` = mean slope in the null world; `cirugias` = surgeries; `con_antes` / `con_despues` = with a measurement before / after surgery; `antes_y_2_despues` = before and at least two after.

## Known limits
- The small JSON parameter files that the notebooks also write (for example `sim3_parametros.json`) were not collected and are not included.
- Some cells of the 27 Oct run showed convergence warnings from the quantile regression; the results are unchanged.

## Reproducing
Open a notebook in Google Colab and choose Runtime, then Run all.
