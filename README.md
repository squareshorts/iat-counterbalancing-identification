# IAT Pairing-Position Identification Analysis

This repository contains the reproducible analysis code and compact result files supporting the study:

**Pairing and block position are not separately identified in the Implicit Association Test: consequences for group comparisons**

## Scope

The repository reproduces the numerical results reported in the manuscript.

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

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

## Reproduction workflow

1. Download the Age IAT data:

python -m src.data.download_age_iat

2. Prepare the Age IAT data:

python -m src.data.prepare_age_iat

3. Place the Gender-Science source files under:

data/GenderScience_iat_2019/iat_2019/

Expected filenames:

- iat.txt
- iat2.txt
- iat.0003.txt

4. Build block-level aggregates:

python scripts\build_block_aggregates.py

5. Run the primary analysis:

python scripts\analyse.py

Large intermediate and participant-level files are generated locally and excluded from Git.

## Main outputs

- results/summary_measures.csv
- results/cell_means.csv
- results/bias_table.csv
- results/reliability.csv

## License

The analysis software is released under the MIT License. Source datasets remain governed by their original repository terms.
