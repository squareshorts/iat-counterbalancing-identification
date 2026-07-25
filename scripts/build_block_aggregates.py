"""Per-participant, per-block sufficient statistics for the counterbalancing analysis.

One row per (dataset, pid, block, pairing) with what is needed for
(a) correct-trial mean log latency, (b) the conventional D score, (c) error rates.

Latency window 300-10000 ms; critical combined-task blocks 3, 4, 6, 7.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

CRITICAL = [3, 4, 6, 7]
RT_LO, RT_HI = 300, 10000

# Explicit compatibility coding (not inferred from alphabetical order).
GS_CONGRUENT = "Science/Male,Liberal Arts/Female"
GS_INCONGRUENT = "Liberal Arts/Male,Science/Female"

AGGCOLS = ["n_all", "rt_sum", "rt_sumsq", "n_err", "n_ok", "logrt_sum"]


def _agg_chunk(df):
    df = df[df["block"].isin(CRITICAL)]
    df = df[(df["rt"] >= RT_LO) & (df["rt"] <= RT_HI)]
    df = df.dropna(subset=["pairing"])
    if df.empty:
        return pd.DataFrame()
    correct = df["trial_error"] == 0
    rt = df["rt"].astype("float64")
    df = df.assign(n_all=1, rt_sum=rt, rt_sumsq=rt ** 2,
                   n_err=(~correct).astype("int64"), n_ok=correct.astype("int64"),
                   logrt_sum=np.where(correct, np.log(rt), 0.0))
    return df.groupby(["pid", "block", "pairing"], observed=True)[AGGCOLS].sum().reset_index()


def _combine(parts):
    out = pd.concat(parts, ignore_index=True)
    return out.groupby(["pid", "block", "pairing"], observed=True)[AGGCOLS].sum().reset_index()


def build_gender_science():
    src = ROOT / "data" / "GenderScience_iat_2019" / "iat_2019"
    usecols = ["block_number", "block_pairing_definition", "trial_latency", "trial_error", "session_id"]
    parts = []
    for name in ["iat.txt", "iat2.txt", "iat.0003.txt"]:
        path = src / name
        if not path.exists():
            print(f"  missing {path}")
            continue
        print(f"  streaming {name}", flush=True)
        reader = pd.read_csv(path, sep="\t", usecols=usecols, chunksize=2_000_000,
                             low_memory=False, on_bad_lines="skip")
        for i, chunk in enumerate(reader):
            chunk.columns = [c.strip() for c in chunk.columns]
            chunk = chunk.rename(columns={"block_number": "block",
                                          "block_pairing_definition": "pairing_raw",
                                          "trial_latency": "rt", "session_id": "pid"})
            praw = chunk["pairing_raw"].astype(str).str.strip()
            chunk["pairing"] = np.where(praw == GS_CONGRUENT, "congruent",
                                np.where(praw == GS_INCONGRUENT, "incongruent", None))
            for col in ("block", "rt", "trial_error", "pid"):
                chunk[col] = pd.to_numeric(chunk[col], errors="coerce")
            chunk = chunk.dropna(subset=["block", "rt", "trial_error", "pid"])
            chunk["block"] = chunk["block"].astype("int16")
            chunk["rt"] = chunk["rt"].astype("int32")
            chunk["trial_error"] = chunk["trial_error"].astype("int8")
            chunk["pid"] = chunk["pid"].astype("int64")
            got = _agg_chunk(chunk)
            if not got.empty:
                parts.append(got)
            if len(parts) >= 6:
                parts = [_combine(parts)]
            print(f"    chunk {i}", flush=True)
    out = _combine(parts)
    out.insert(0, "dataset", "Gender-Science")
    return out


def _age_label(left):
    s = str(left).lower()
    if "old" in s and "bad" in s:
        return "congruent"
    if "young" in s and "good" in s:
        return "congruent"
    if "old" in s and "good" in s:
        return "incongruent"
    if "young" in s and "bad" in s:
        return "incongruent"
    return None


def build_age():
    path = ROOT / "data" / "processed" / "age_iat" / "age_iat_trials_standardized.parquet"
    pf = pq.ParquetFile(path)
    cols = ["pid", "block", "rt_raw_ms", "trial_error", "category", "block_name"]
    parts = []
    for rg in range(pf.metadata.num_row_groups):
        chunk = pf.read_row_group(rg, columns=cols).to_pandas()
        chunk = chunk.rename(columns={"rt_raw_ms": "rt"})
        chunk = chunk[chunk["block"].isin(CRITICAL)]
        if chunk.empty:
            continue
        keys = (chunk[["pid", "block", "category", "block_name"]].drop_duplicates()
                .groupby(["pid", "block", "category"], observed=True)["block_name"]
                .agg(lambda s: "|".join(pd.unique(s))).unstack("category").reset_index())
        keys["pairing"] = keys["left"].map(_age_label)
        keys = keys[["pid", "block", "pairing"]].dropna()
        merged = chunk[["pid", "block", "rt", "trial_error"]].merge(keys, on=["pid", "block"], how="inner")
        got = _agg_chunk(merged)
        if not got.empty:
            parts.append(got)
        if len(parts) >= 6:
            parts = [_combine(parts)]
        print(f"  age row group {rg + 1}/{pf.metadata.num_row_groups}", flush=True)
    out = _combine(parts)
    out.insert(0, "dataset", "Age")
    return out


if __name__ == "__main__":
    print("Age")
    age = build_age()
    age.to_csv(OUT / "block_aggregates_age.csv", index=False)
    print(f"  {age['pid'].nunique()} participants, {len(age)} rows")
    print("Gender-Science")
    gs = build_gender_science()
    gs.to_csv(OUT / "block_aggregates_gender_science.csv", index=False)
    print(f"  {gs['pid'].nunique()} participants, {len(gs)} rows")
