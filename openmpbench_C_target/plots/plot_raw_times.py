#!/usr/bin/env python3
"""
scatter4.py

What it does
- Parses *your* distribution file (handles the "missing orep header" situation)
- Parses your overhead txt file (the [Method=...] blocks + Set/Run/Lmin/Intercept/Slope lines)
- Plots ONE figure:
    scatter points from distribution (4 colours by (set,run) = (0,0)(0,1)(1,0)(1,1))
    + overlays regression lines from overhead (a + b*x) starting at Lmin
- Default: ALL delaylength + log2 x-axis
- Your manifest:
    python3 scatter4.py distribution.csv overhead.txt 1,4 lin
      -> only include the 1st..4th UNIQUE delaylength values (sorted)
      -> use linear x-axis

Usage
  python3 scatter4.py <distribution> <overhead> [i,j] [lin|log] [out.png]

Examples
  python3 scatter4.py distribution.csv overhead.txt
  python3 scatter4.py distribution.csv overhead.txt 1,4 lin
  python3 scatter4.py distribution.csv overhead.txt 1,8 log myplot.png
"""

import sys, os, re, csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -------------------------
# Style
# -------------------------
def apply_style():
    plt.rcParams.update({
        "figure.figsize": (7.6, 4.8),
        "figure.dpi": 160,
        "savefig.dpi": 300,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 12,
        "legend.fontsize": 7,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


# -------------------------
# Parsers
# -------------------------
def load_distribution_csv(path: str) -> pd.DataFrame:
    """
    Robust parser for distribution CSVs that may have:
      - 9 headers but 10 fields per row (extra orep column)
      - or proper 10 headers
      - or 9 fields per row (no orep)
    Expected final columns:
      method_id, method_name, N, thread_count, team_count, set, run, delaylength, orep, exec_time_us
    """
    rows = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"Empty distribution file: {path}")

        for r in reader:
            if not r:
                continue

            # Common case in your file: 10 fields but only 9 headers
            if len(r) == 10:
                method_id, method_name, N, th, tm, setv, runv, delay, orep, exec_us = r
            elif len(r) == 9:
                method_id, method_name, N, th, tm, setv, runv, delay, exec_us = r
                orep = 0
            else:
                # skip malformed lines
                continue

            rows.append([
                int(method_id),
                str(method_name),
                int(N),
                int(th),
                int(tm),
                int(setv),
                int(runv),
                float(delay),
                int(orep),
                float(exec_us),
            ])

    df = pd.DataFrame(rows, columns=[
        "method_id","method_name","N","thread_count","team_count",
        "set","run","delaylength","orep","exec_time_us"
    ])
    return df


def load_overhead_txt(path: str) -> pd.DataFrame:
    """
    Parses overhead txt like:
      [Method=6 teams distribute parallel for N=16382]
      Set=0 Run=0  Lmin=41850  Intercept=484.015647μs  Slope=0.783638  R2=... BIC=...
    Returns columns:
      method_id, method_name, N, set, run, Lmin, intercept_us, slope
    """
    rows = []
    current = {}

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            m = re.match(r"^\[?Method=(\d+)\s+(.+)\s+N=(\d+)\]?$", line)
            if m:
                current = {
                    "method_id": int(m.group(1)),
                    "method_name": m.group(2).strip(),
                    "N": int(m.group(3)),
                }
                continue

            m2 = re.search(
                r"Set=(\d+)\s+Run=(\d+)\s+Lmin=([-\d\.]+)\s+Intercept=([-\d\.]+)\s*(?:μs|us)(?:\s+Lowest=([-\d\.]+)\s*(?:μs|us))?\s+Slope=([-\d\.]+)",
                line
            )

            if m2 and current:
                rows.append({
                    **current,
                    "set": int(m2.group(1)),
                    "run": int(m2.group(2)),
                    "Lmin": float(m2.group(3)),
                    "intercept_us": float(m2.group(4)),
                    "lowest": float(m2.group(5)) if m2.group(5) is not None else None,
                    "slope": float(m2.group(6)),
                })
    return pd.DataFrame(rows)


# -------------------------
# Manifest: choose delaylength subset
# -------------------------
def pick_delaylengths(dist, spec):
    """
    spec:
      None -> all delaylengths
      "i,j" -> take unique delaylengths sorted, slice [i-1 : j] (1-indexed, inclusive)
    """
    uniq = sorted(dist["delaylength"].unique())
    if spec is None:
        return uniq

    m = re.match(r"^\s*(\d+)\s*,\s*(\d+)\s*$", spec)
    if not m:
        raise ValueError("Delay spec must look like '1,4' (1-indexed inclusive).")

    i = int(m.group(1))
    j = int(m.group(2))
    if i < 1 or j < i:
        raise ValueError("Delay spec invalid: must satisfy 1 <= i <= j.")

    return uniq[i-1:j]


# -------------------------
# Plot (4 colours + overhead lines)
# -------------------------
def plot(dist: pd.DataFrame, ovh: pd.DataFrame, out_png: str, scale: str, delay_spec):
    # Keep only 4 groups
    keep = {(0, 0), (0, 1), (1, 0), (1, 1)}
    dist = dist[dist.apply(lambda r: (int(r["set"]), int(r["run"])) in keep, axis=1)].copy()
    if dist.empty:
        raise SystemExit("No rows after filtering to 4 groups: (set,run) in {(0,0),(0,1),(1,0),(1,1)}")

    # Delay subset
    chosen = pick_delaylengths(dist, delay_spec)
    dist = dist[dist["delaylength"].isin(chosen)].copy()
    if dist.empty:
        raise SystemExit("No rows left after applying delaylength subset.")

    # Match overhead to this method/N and 4 groups
    method_id = int(dist["method_id"].iloc[0])
    N = int(dist["N"].iloc[0])
    method_name = str(dist["method_name"].iloc[0])
    th = int(dist["thread_count"].iloc[0])
    tm = int(dist["team_count"].iloc[0])

    if not ovh.empty:
        ovh = ovh[(ovh["method_id"] == method_id) & (ovh["N"] == N)].copy()
        ovh = ovh[ovh.apply(lambda r: (int(r["set"]), int(r["run"])) in keep, axis=1)].copy()

    palette = {(0, 0): "gold", (0, 1): "purple", (1, 0): "red", (1, 1): "blue"}
    label = {(0, 0): "yellow (Set0 Run0)", (0, 1): "purple (Set0 Run1)",
             (1, 0): "red (Set1 Run0)",   (1, 1): "blue (Set1 Run1)"}

    fig, ax = plt.subplots()

    for (s, r), sub in dist.groupby(["set", "run"], sort=True):
        key = (int(s), int(r))
        c = palette[key]

        # Scatter points
        ax.scatter(sub["delaylength"], sub["exec_time_us"],
                   s=18, alpha=0.35, color=c,
                   label=f"{label[key]} points")

        # Overhead line (authoritative): y = a + b*x from Lmin onwards
        if not ovh.empty:
            row = ovh[(ovh["set"] == s) & (ovh["run"] == r)]
            if len(row) == 1:
                a = float(row["intercept_us"].iloc[0])
                b = float(row["slope"].iloc[0])
                lmin = float(row["Lmin"].iloc[0])

                xmin = max(lmin, float(sub["delaylength"].min()))
                xmax = float(sub["delaylength"].max())
                if xmax > xmin:
                    xs = np.linspace(xmin, xmax, 200)
                    ys = a + b * xs
                    ax.plot(xs, ys, linewidth=2.5, color=c,
                            label=f"{label[key]} fit (a={a:.1f}μs, b={b:.4f}, Lmin={int(lmin)})")

    # Axis scaling
    if scale == "log":
        ax.set_xscale("log", base=2)
        ax.set_xlabel("Delaylength (log2 scale)")
        ax.set_yscale("log", base=2)
        ax.set_ylabel("Execution time (μs) (log2 scale)")
    else:
        ax.set_xlabel("Delaylength (linear scale)")
        ax.set_ylabel("Execution time (μs)")

    ax.set_title(f"Exec time vs delaylength — Method {method_id}, N={N}, thread={th}, teams={tm}")
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
    fig.savefig(out_png)
    plt.close(fig)


# -------------------------
# Entry
# -------------------------
def main():
    apply_style()

    if len(sys.argv) < 3:
        print(__doc__.strip())
        raise SystemExit(2)

    dist_path = sys.argv[1]
    ovh_path = sys.argv[2]
    delay_spec = sys.argv[3] if len(sys.argv) >= 4 else None
    scale = sys.argv[4].lower().strip() if len(sys.argv) >= 5 else "log"
    out_png = sys.argv[5] if len(sys.argv) >= 6 else "4colorDist"+delay_spec+".png"

    if scale not in ("lin", "log"):
        raise SystemExit("scale must be 'lin' or 'log'")

    dist = load_distribution_csv(dist_path)
    ovh = load_overhead_txt(ovh_path) if os.path.exists(ovh_path) else pd.DataFrame()

    plot(dist, ovh, out_png, scale=("lin" if scale == "lin" else "log"), delay_spec=delay_spec)

    print(f"[OK] saved: {out_png}")
    if delay_spec:
        uniq = sorted(dist["delaylength"].unique())
        chosen = pick_delaylengths(dist, delay_spec)
        # print(f"[INFO] delay_spec='{delay_spec}' means unique delays sorted = {uniq}")
        # print(f"[INFO] chosen delays = {chosen}")
    print(f"[INFO] x-scale = {scale}")


if __name__ == "__main__":
    main()
