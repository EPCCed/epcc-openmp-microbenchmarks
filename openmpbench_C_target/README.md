# OpenMP target-offload microbenchmark

This C/OpenMP suite accompanies "A Microbenchmark Suite for OpenMP Target Offload" by Weiyu Tu, J. Mark Bull and James Richings (IWOMP 2026). It measures host-observed costs of target regions, data mapping, device parallelism, atomics and reductions. It is separate from the CPU suites in this repository.

The benchmark source, Makefile and compiler definitions were copied byte-for-byte from [research snapshot commit `85eddd9`](https://github.com/SniperNov/IWOMP-Microbenchmarking-snapshot/tree/85eddd9aa5e41994ef998eac8156fb96538ea712), created on 24 June 2026. The plotting helper has only comment and whitespace cleanup. This directory excludes machine-specific batch scripts, generated binaries and measurement results. The published paper is authoritative for its reported methodology and results; this source snapshot does not by itself establish the exact binary or command line used for every published point.

## Contents

| Path | Purpose |
| --- | --- |
| `src/microbenchmark.c` | Twelve OpenMP target-offload methods and timing summaries. |
| `src/common.c`, `src/common.h` | Delay kernel and shared declarations. |
| `Makefile`, `Makefile.defs.*` | Build rules and compiler-specific examples. |
| `plots/plot_raw_times.py` | Optional diagnostic plot of raw times and fitted lines. |

## Build

The Makefile defaults to `Makefile.defs.nvc`. Before building with another compiler, change its first `include` line to the appropriate `Makefile.defs.*` file and adjust the compiler path, GPU target architecture and flags for your system. The supplied definitions cover NVHPC, GCC, Cray and AMD Clang configurations. Build on a machine with the intended OpenMP offload toolchain:

```sh
make clean
make distribution
```

This produces `microbenchmark_distribution`; `make` alone produces `microbenchmark`. The distribution build includes per-run fit details in its output.

## Run

Run inside a GPU allocation, with offload required so that a host fallback is not mistaken for a GPU result:

```sh
OMP_TARGET_OFFLOAD=mandatory ./microbenchmark_distribution \
  Method=0,5,6,7,10 N=16384 Delay=1,8096 \
  thread_count=32 team_count=4
```

`Method`, `N`, `thread_count` and `team_count` accept comma-separated values. `Delay=min,max` selects the delay range. For Methods 1-4, `N` is the mapped element count; for Methods 8-9 it is the shared-array size; for Method 11 it is the number of inner parallel regions. Select thread and team counts appropriate for the device.

| Method | Construct |
| --- | --- |
| 0 | `target` |
| 1-4 | `target` with `map(tofrom:)`, `map(to:)`, `map(from:)` or `map(alloc:)` |
| 5 | `target teams` |
| 6 | `target teams distribute parallel for` |
| 7 | `target nowait` followed by `taskwait` |
| 8 | Distributed loop with atomic updates |
| 9 | Distributed loop with an array-section reduction |
| 10 | `target teams` with a separate `parallel` region |
| 11 | `target teams` with repeated `parallel` regions |

The executable writes `raw_times.csv` in the current directory, replacing any existing CSV of that name. It appends summaries to `overhead_distribution.txt`, so remove or move that file before starting a new experiment. Standard output reports both a BIC-selected intercept and `Lowest`; these are different summaries.

The optional plot helper requires NumPy, pandas and Matplotlib. For example:

```sh
python3 plots/plot_raw_times.py raw_times.csv overhead_distribution.txt 1,18 lin result.png
```

## Reproducibility notes

This preserved snapshot uses 20 logarithmically spaced delay points over 1-8096, with two sets of five runs per point. Its printed `Lowest` is the average of the minimum delay-point timing from each run. The paper describes powers-of-two delays through 8192 and the minimum of the per-delay sample means. The ten repeated measurements per point are not the same quantity as the 20 delay points. Reproducing a published result requires the original source revision, compiler and flags, GPU, runtime environment, command line and raw measurements.

Methods 6 and 9 contain compiler-conditional code. In this preserved snapshot, their explicit branches cover NVHPC and Cray/AMD/Clang, but not plain GCC; without a matching macro the switch falls through to the next method. The Clang-side Method 9 branch also contains two pragmas without `omp`, which Clang ignores. The source is kept unchanged for provenance. Validate the generated code and behaviour on your compiler before using it to compare these constructs.

The target-offload directory has no separate licence declaration. Please confirm reuse terms with the EPCC repository maintainers; licences in the CPU-suite directories do not automatically apply here.
