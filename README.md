# IAT Pairing-Position and Sequence-Allocation Analysis

This repository contains the reproducible analysis code and compact result files supporting the study:

**Pairing, position, and sequence allocation in the Implicit Association Test: exact identities and consequences for group comparisons**

## Scope

The repository reproduces the numerical results reported in the manuscript. The analysis treats the equal-sequence marginal of the reported score and the sequence contrast as distinct estimands and quantifies how sequence allocation changes pooled estimates.

Included:

- scripts for downloading and preparing the public Age IAT data
- scripts for constructing block-level sufficient statistics
- the primary analysis script
- compact summary outputs reported in the manuscript
- dependency and data-source documentation

Not included:

- raw Project Implicit data
- participant-level derived data
- large block-level intermediate files
- manuscript or supplementary LaTeX files
- temporary files and logs

## Public data sources

Gender-Science IAT: https://osf.io/cfvyj/

Age IAT: https://osf.io/9jvmk/

Raw data remain subject to the terms of the original repositories and are not redistributed here.

## Installation

Run these commands from the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Reproduction workflow

1. Download the Age IAT data:

```powershell
python -m src.data.download_age_iat
```

2. Prepare the Age IAT data:

```powershell
python -m src.data.prepare_age_iat
```

3. Place the Gender-Science source files under:

```text
data/GenderScience_iat_2019/iat_2019/
```

Expected filenames:

- `iat.txt`
- `iat2.txt`
- `iat.0003.txt`

4. Build block-level aggregates:

```powershell
python scripts\build_block_aggregates.py
```

5. Run the primary analysis:

```powershell
python scripts\analyse.py
```

Large intermediate and participant-level files are generated locally and excluded from Git.

## Main outputs

- `results/summary_measures.csv`
- `results/cell_means.csv`
- `results/bias_table.csv` (legacy filename; contains deterministic sequence-allocation sensitivity calculations)
- `results/reliability.csv`

The repository does not contain an executed participant-level subgroup allocation audit. Accordingly, it supports exact allocation identities and dataset-level sequence contrasts, not observed allocation-induced components for demographic or archival subgroup comparisons.

## Release

Version 2.0.4 aligns the repository title, terminology, and release metadata with the finalized manuscript framing. See `CHANGELOG.md`.

## License

The analysis software is released under the MIT License. Source datasets remain governed by their original repository terms.
