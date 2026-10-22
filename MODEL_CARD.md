# Model Card — Reduced Biological State Index (BSI), NHANES 1999-2002

## 1. Model details

Reduced Biological State Index (BSI) and the Cox proportional-hazards models that test its added value. Author: Aly Gallo Lopez (doctoral student, Deep Tech, UNMSM). Version: notebook v4.1 re-run in this notebook (2026-10). BSI = equal-weight mean of three standardized domain scores: inflammation (log C-reactive protein, log urinary albumin/creatinine ratio), metabolism (glucose, log insulin, log triglycerides, HbA1c, minus HDL) and epigenetic-age acceleration (PhenoAge residual on age). Compared models: M1 age+sex; M2 +epigenetic clock acceleration; M3 +simplified allostatic load; M4 +BSI. Cox models with ridge penalizer 1e-4. Software: {'lifelines': '0.30.3', 'scikit-learn': '1.6.1', 'pandas': '2.2.3', 'numpy': '2.1.3', 'python': '3.13.16'}. License of this code: UNKNOWN — to investigate. Contact: see repository.

## 2. Intended use

Research use only: to test whether a composite of routine biomarkers adds prognostic information for all-cause mortality over age, sex, an epigenetic clock and allostatic load, as an exploratory step of the ChroniCare-AI doctoral project. Out-of-scope / misuse: individual clinical decisions, insurance or employment risk scoring, any claim about Adaptive Capacity (this analysis has no perturbation and no recovery), any claim about biological aging beyond the PhenoAge acceleration used as one input, and use in people younger than 50 or outside the US population sampled.

## 3. Relevant factors

Age and sex are model covariates; race/ethnicity and age group are used only for subgroup reporting. Missingness differs by marker (fasting subsample for insulin, glucose, triglycerides), which can correlate with health status. Instrumentation: NHANES 1999-2002 laboratory assays; DNA methylation measured on Illumina MethylationEPIC v1.0 arrays at Duke University from whole blood stored at -80 C (CDC documentation). The methylation sample is a subsample: about half of the eligible non-Hispanic White participants and all eligible participants of the other groups, so it over-represents non-White groups relative to the US population. Assay comparability with current laboratories is UNKNOWN — to investigate.

## 4. Metrics

Concordance index (C) of out-of-fold Cox risk, 5-fold cross-validation repeated 5 times with the same folds for all models. Primary metric: dC = C(M4) - C(M3) with a paired bootstrap 95% CI (2,000 replications). Decision rule fixed before seeing results: ADDS if the lower limit > 0; DOES NOT ADD if the CI lies inside +/-0.01; INCONCLUSIVE otherwise. Also reported: hazard ratio of the BSI per 1 SD, proportional-hazards test, survey-weighted hazard ratio, complete-case analysis and a control against the same markers entered as continuous variables. Calibration and net benefit were not assessed: UNKNOWN — to investigate.

## 5. Evaluation data

Same dataset as training, evaluated out-of-fold (no external validation). NHANES 1999-2000 and 2001-2002, adults aged 50 or older in the CDC DNA-methylation release, with linked mortality; primary analysis n=2530 with 1359 deaths. See DATASHEET.md. External validation in an independent population: not done (planned for the Rebagliati cohort within the thesis protocol).

## 6. Training data

Same NHANES sample; the Cox models are fitted inside each cross-validation fold. The BSI itself has no fitted weights (equal-weight mean of z-scores, no outcome label used); its standardization parameters and the allostatic-load quartile cut-points are computed in the whole analysed sample, which is a minor source of optimism. No separate held-out set.

## 7. Quantitative analyses

Primary (n=2530, deaths=1359): C(M1)=0.7078, C(M2)=0.7124, C(M3)=0.7161, C(M4)=0.7232; dC = 0.0071, 95% CI (0.0033 to 0.0108) -> ADDS. Hazard ratio of the BSI per 1 SD, adjusted: 1.332 (1.207 to 1.471); proportional-hazards test for the BSI p=0.0018; survey-weighted HR 1.299 (1.091 to 1.547) (approximate weights).
Complete cases (n=1228, deaths=644): dC(M4-M3) = 0.0054, 95% CI (0.0015 to 0.0095). Control against the same 7 markers as continuous variables: dC(M4-M6) = -0.0025, 95% CI (-0.0088 to 0.0039) -> DOES NOT ADD: the composite did not outperform its own markers.
Exercise 1 (baselines, same grid for both models): gain of M4 over the weak age+sex baseline = 0.0155; over M3 with default penalizer = 0.0070; over M3 with both tuned = 0.0069. Tuning the ridge penalizer changed C by at most 0.0004 for either model, so in this low-dimensional Cox model the result does not depend on tuning; the weak-versus-tuned lesson matters mainly for flexible models (PE1-PE2).
Exercise 2 (seeds): dC over 10 seeds = 0.0071 +/- 0.0003 (min 0.0066, max 0.0076); positive in 10/10 seeds. The SD reflects only the assignment of cross-validation folds, not the sampling variability of the data, which is what the bootstrap interval captures.
Exercise 3 (ablation, exploratory):
- full BSI (3 domains): dC vs M3 = 0.0071 +/- 0.0003 (SD over 10 seeds); drop vs full BSI = 0.0000 +/- 0.0000
- without inflammation: dC vs M3 = -0.0005 +/- 0.0004 (SD over 10 seeds); drop vs full BSI = 0.0076 +/- 0.0005
- without metabolism: dC vs M3 = 0.0112 +/- 0.0002 (SD over 10 seeds); drop vs full BSI = -0.0041 +/- 0.0003
- without epigenetic acceleration: dC vs M3 = 0.0071 +/- 0.0003 (SD over 10 seeds); drop vs full BSI = -0.0000 +/- 0.0000
- inflammation only: dC vs M3 = 0.0112 +/- 0.0002 (SD over 10 seeds); drop vs full BSI = -0.0041 +/- 0.0003
- metabolism only: dC vs M3 = -0.0005 +/- 0.0004 (SD over 10 seeds); drop vs full BSI = 0.0076 +/- 0.0005
Because the epigenetic-clock acceleration is already a covariate in every model, dropping a domain from the BSI is algebraically equivalent (up to the tiny ridge penalty) to: without epigenetic acceleration = the full BSI (identical by construction, so that row carries no information); without metabolism = the inflammation domain alone; without inflammation = the metabolic domain alone. Reading: the added value comes from the inflammatory domain (inflammation alone dC = 0.0112); the metabolic domain alone adds nothing (dC = -0.0005), probably because its five markers are already counted in the allostatic load, and it dilutes the equal-weight composite. This is a post hoc exploratory finding: the BSI definition (equal-weight mean of all domains) is NOT changed after seeing it, to avoid cherry-picking and HARKing.
Subgroups (out-of-fold predictions of the primary analysis):
- Sex: male: n=1284, deaths=739, dC=0.0033 (95% CI -0.0018 to 0.0083)
- Sex: female: n=1246, deaths=620, dC=0.0119 (95% CI 0.0065 to 0.0177)
- Age 50-64: n=1194, deaths=350, dC=0.0162 (95% CI 0.0011 to 0.0323)
- Age 65+: n=1336, deaths=1009, dC=0.0108 (95% CI 0.0046 to 0.0181)
- Race/ethnicity: Mexican American: n=720, deaths=346, dC=0.0151 (95% CI 0.0057 to 0.0251)
- Race/ethnicity: Other Hispanic: n=163, deaths=70, dC=0.0072 (95% CI -0.0096 to 0.0242)
- Race/ethnicity: Non-Hispanic White: n=1026, deaths=603, dC=0.0040 (95% CI -0.0003 to 0.0084)
- Race/ethnicity: Non-Hispanic Black: n=538, deaths=310, dC=0.0028 (95% CI -0.0074 to 0.0143)
- Race/ethnicity: Other/multiracial: n=83, deaths=30, dC=0.0021 (95% CI -0.0259 to 0.0274)
Point estimates are positive in 9 of 9 subgroups; the 95% CI excludes zero in: Sex: female, Age 50-64, Age 65+, Race/ethnicity: Mexican American. These are descriptive: no interaction tests and no multiplicity correction were done, the subgroups are small, and differences between subgroups are not established.
Second evaluation, MIDUS 3 Biomarker Project (ICPSR 38837), from notebook BSI_MIDUS3_respuesta_al_reto, not re-run here: resting BSI (inflammatory, metabolic and neuroendocrine domains, no epigenetic clock) did not improve out-of-fold prediction of heart-rate-variability reactivity to a mental-arithmetic task beyond age, sex, BMI, baseline level, antihypertensive and beta-blocker use and allostatic load (n=521; dR2 +0.0004, 95% CI -0.0082 to 0.0090, DOES NOT ADD). Cortisol reactivity (n=639; dR2 -0.0040) and HRV on standing (n=483; dR2 -0.0017) also showed no gain; systolic-pressure reactivity was not interpretable (out-of-fold R2 below zero).

## 8. Ethical considerations

Public-use, de-identified data; no contact with participants. A mortality-related score can be misused for discrimination (insurance, employment) or be read as a personal prognosis; it must not be used that way. Subgroup performance is reported to avoid hiding differences by sex, age and race/ethnicity, but cells are small. The author is Scientific Director of a company (ADAPTIVE Health OS) for which the broader project is conceived as an engine; this conflict of interest is declared and the null results are reported as findings.

## 9. Caveats and recommendations

(1) The gain is small (dC about 0.0071) and does not exceed the same markers used as continuous variables. (2) The proportional-hazards assumption does not hold for the BSI (p=0.0018), so a single hazard ratio is an average over follow-up. (3) PhenoAge shares markers with the BSI. (4) The bootstrap interval ignores the variability of model fitting; z-score parameters and quartile cut-points use the whole sample. (5) Reduced BSI: no cortisol, no BDNF. (6) All-cause mortality is the only outcome. (7) One cross-sectional snapshot: this does NOT test Adaptive Capacity. (8) Exercises 1-3 and subgroups are exploratory, run after the primary analysis was fixed, on the same data; the domain ablation is post hoc and does not change the BSI definition. (9) No external validation and no calibration assessment. (10) The CDC documentation instructs analysts to use the sample weights (WTDN4YR) for all analyses; the primary analysis is unweighted and the weighted hazard ratio is only a sensitivity analysis, so the results describe this subsample, not the US population. (11) The public-use linked mortality file perturbs some follow-up times and causes of death with synthetic values (vital status is unchanged), so time-to-event estimates are approximate. Recommendation: do not use the BSI for individual prediction; treat BSI construction as an empirical question (protocol PE1-PE2) and test Adaptive Capacity directly in a perturbation-recovery design (PE3).
