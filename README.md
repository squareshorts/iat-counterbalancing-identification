# Sequence Allocation in the Implicit Association Test

This repository contains analysis code and compact validated outputs supporting the study:

**Sequence allocation in the Implicit Association Test: exact estimands, group heterogeneity, and finite-sample operating characteristics**

## Scope

The analysis distinguishes three quantities that are often conflated in the standard two-sequence IAT design: the equal-sequence marginal of the reported score, the sequence contrast of that score, and the allocation-induced component of a pooled group estimate. It reproduces the Gender–Science and Age IAT benchmarks, reconstructs the public Age score, evaluates observed subgroup allocation effects, compares sequence contrasts across groups, and examines finite-sample operating characteristics by empirical resampling.

The final results show that observed allocation-induced shifts were negligible in the analysed archive, while sequence contrasts differed across groups. Finite-sample disagreements were modest, concentrated on near-null contrasts, and equal-sequence standardization did not improve root mean squared error.

## Included

- the original data-preparation and primary-analysis scripts;
- benchmark-reproduction tables for both datasets;
- reconstructed standardized-score validation;
- Age participant-linkage and sequence-validation diagnostics;
- sequence-specific standardized-score estimates;
- a compact table of the headline subgroup and finite-sample results;
- revised figure captions and the final strengthening audit;
- an execution specification for the complete private analysis workflow.

The full v2.1.0 archival package additionally contains the complete strengthening scripts, detailed subgroup and bootstrap tables, robustness tables, figure source data, and publication figures.

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

## Original analysis workflow

```powershell
python -m src.data.download_age_iat
python -m src.data.prepare_age_iat
python scripts\build_block_aggregates.py
python scripts\analyse.py
```

The Gender–Science source files are expected under `data/GenderScience_iat_2019/iat_2019/`. Large intermediate and participant-level files are generated locally and excluded from Git.

## Strengthening analysis

The complete strengthening workflow is run in the private analysis workspace. Its required inputs, arguments, outputs, seeds, and expected directory structure are documented in `analysis_group_comparison_strengthening/scripts/README_execution.md`. The compact validated outputs retained here permit verification of the manuscript’s headline numerical claims without redistributing participant-level data.

## Principal v2.1.0 outputs

- `analysis_group_comparison_strengthening/results/benchmark_reproduction_age.csv`
- `analysis_group_comparison_strengthening/results/benchmark_reproduction_gender_science.csv`
- `analysis_group_comparison_strengthening/results/standardized_score_sequence_estimates.csv`
- `analysis_group_comparison_strengthening/results/d600_vs_supplied_age.csv`
- `analysis_group_comparison_strengthening/results/age_join_and_order_validation.csv`
- `analysis_group_comparison_strengthening/results/headline_summary.csv`
- `analysis_group_comparison_strengthening/reports/group_comparison_strengthening_audit.md`
- `analysis_group_comparison_strengthening/figures/revised_figure_captions.md`

The original compact outputs remain under `results/` for continuity with version 2.0.4.

## Release

Version 2.1.0 adds the validated benchmark, score-reconstruction, linkage, subgroup-summary, and finite-sample results used in the revised methodological manuscript. See `CHANGELOG.md`.

## License

The analysis software is released under the MIT License. Source datasets remain governed by their original repository terms.
