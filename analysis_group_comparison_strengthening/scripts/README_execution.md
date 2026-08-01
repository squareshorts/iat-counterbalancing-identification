# Running the strengthening pipeline

## Command

From the private analysis workspace, run:

```powershell
python .\analysis_group_comparison_strengthening\scripts\run_strengthening_pipeline.py --root C:\path\to\iat_quantum_analysis
```

To run selected stages:

```powershell
python .\analysis_group_comparison_strengthening\scripts\run_strengthening_pipeline.py --root C:\path\to\iat_quantum_analysis --stages extract,link,blockstats_age,blockstats_gs,scores,benchmarks
```

To list stage names:

```powershell
python .\analysis_group_comparison_strengthening\scripts\run_strengthening_pipeline.py --root C:\path\to\iat_quantum_analysis --list-stages
```

## Arguments

| Argument | Default | Meaning |
|---|---:|---|
| `--root` | required | authoritative private analysis root |
| `--stages` | `all` | comma-separated stage names |
| `--seed` | `20260801` | master random seed |
| `--bootstrap-reps` | `3000` | stratified-bootstrap replicates |
| `--sim-reps` | `5000` | finite-sample replicates per condition |
| `--force` | off | recompute cached intermediates |
| `--list-stages` | off | print stage names and exit |

## Required source files

All paths are resolved beneath `--root`:

```text
data\GenderScience_iat_2019\iat_2019\iat.txt
data\GenderScience_iat_2019\iat_2019\iat2.txt
data\GenderScience_iat_2019\iat_2019\iat.0003.txt
data\processed\age_iat\age_iat_trials_standardized.parquet
data\age_netherlands\Age IAT.public.2002-2021.csv
data\age_netherlands\Age_IAT_public_2002-2024_codebook.xlsx
```

The source datasets are not redistributed in this repository. The pipeline stops with an informative error when a required path is absent and never modifies raw data.

## Outputs

The pipeline writes compact tables, figures, reports, logs, and environment metadata beneath `analysis_group_comparison_strengthening/`.

## Determinism

The master seed is recorded in the execution log. Bootstrap and simulation stages use independent seeds derived through `numpy.random.SeedSequence`.
