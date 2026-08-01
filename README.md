# Sequence Allocation in the Implicit Association Test

This repository contains the reproducible analysis code and compact outputs supporting the study:

**Sequence allocation in the Implicit Association Test: exact estimands, group heterogeneity, and finite-sample operating characteristics**

## Scope

The analysis distinguishes three quantities that are often conflated in the standard two-sequence IAT design: the equal-sequence marginal of the reported score, the sequence contrast of that score, and the allocation-induced component of a pooled group estimate. It reproduces the original Gender–Science and Age IAT benchmarks, reconstructs the public Age score, evaluates observed subgroup allocation effects, tests pairwise heterogeneity in the sequence contrast, and examines finite-sample operating characteristics by empirical resampling.

The final results show that observed allocation-induced shifts were negligible in the analysed archive, while sequence contrasts differed across groups. Finite-sample disagreements were modest, concentrated on near-null contrasts, and equal-sequence standardization did not improve root mean squared error.

## Included

- scripts for preparing the public Age and Gender–Science IAT data;
- the complete strengthening-analysis pipeline;
- benchmark-reproduction tables for both datasets;
- reconstructed standardized-score validation;
- subgroup estimands and pairwise comparisons;
- bootstrap heterogeneity tests with false-discovery-rate correction;
- age-band sensitivity analyses;
- finite-sample resampling results;
- robustness summaries, figure source data, and the final audit report.

## Not included

- raw Project Implicit data;
- participant-level derived data;
- large block-level caches;
- manuscript or submission files;
- temporary files and logs containing local paths.

## Public data sources

- Gender–Science IAT: https://osf.io/cfvyj/
- Age IAT: https://osf.io/9jvmk/

Raw data remain governed by the terms of the original repositories and are not redistributed here.

## Installation

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Main workflow

The complete strengthening analysis is run from the private analysis workspace with:

```powershell
python analysis_group_comparison_strengthening\scripts\run_strengthening_pipeline.py --root C:\path\to\iat_quantum_analysis --bootstrap-reps 3000 --sim-reps 5000 --seed 20260801
```

The script validates required inputs, reproduces the benchmark results, runs the subgroup and resampling analyses, creates figures, and writes the audit report. See `analysis_group_comparison_strengthening/scripts/README_execution.md` for details.

## Principal outputs

- `analysis_group_comparison_strengthening/results/benchmark_reproduction_age.csv`
- `analysis_group_comparison_strengthening/results/benchmark_reproduction_gender_science.csv`
- `analysis_group_comparison_strengthening/results/standardized_score_sequence_estimates.csv`
- `analysis_group_comparison_strengthening/results/subgroup_estimands.csv`
- `analysis_group_comparison_strengthening/results/subgroup_pairwise_contrasts.csv`
- `analysis_group_comparison_strengthening/results/gamma_heterogeneity_tests.csv`
- `analysis_group_comparison_strengthening/results/age_band_sensitivity.csv`
- `analysis_group_comparison_strengthening/results/finite_sample_resampling.csv`
- `analysis_group_comparison_strengthening/results/robustness_summary.csv`
- `analysis_group_comparison_strengthening/reports/group_comparison_strengthening_audit.md`

The original compact outputs remain under `results/` for continuity with version 2.0.4.

## Release

Version 2.1.0 adds the validated subgroup, bootstrap, sensitivity, and finite-sample analyses used in the revised methodological manuscript. See `CHANGELOG.md`.

## License

The analysis software is released under the MIT License. Source datasets remain governed by their original repository terms.
