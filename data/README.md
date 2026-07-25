# Data

Raw Project Implicit trial-level data are not included in this repository.

## Gender-Science IAT

Public source:

https://osf.io/cfvyj/

Place the original files at:

data/GenderScience_iat_2019/iat_2019/

Expected filenames:

- iat.txt
- iat2.txt
- iat.0003.txt

## Age IAT

Public source:

https://osf.io/9jvmk/

The current aggregation script expects the locally prepared file:

data/processed/age_iat/age_iat_trials_standardized.parquet

This prepared file is not distributed. It must be generated locally from the public Age IAT source data before running the full reproduction pipeline.

## Reproduction sequence

1. Obtain the public source data.
2. Prepare the Age IAT standardized Parquet file.
3. Run:

   python scripts/build_block_aggregates.py

4. Run:

   python scripts/analyse.py

The scripts generate the large intermediate CSV files locally. These files are excluded from Git by `.gitignore`.
