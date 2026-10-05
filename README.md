# EPCC OpenMP Microbenchmark Suite

This repository contains the source code for the EPCC OpenMP microbenchmark suite. The directory `openmpbench_C_v31` contains Version 3.1, the "classic" version previously available from the EPCC website.
The directory `openmpbench_C_v40` contains Version 4.0, which has additional measurements, improved user control, more sensible defaults and additional statistics reporting.

The directory [openmpbench_C_target](openmpbench_C_target/) contains the OpenMP GPU target-offload microbenchmark associated with the IWOMP 2026 paper by Weiyu Tu, J. Mark Bull and James Richings. It has its own build and reproducibility notes.

Please see the README files in each directory for more details.


## Related Publications

J. M. Bull, Measuring Synchronisation and Scheduling Overheads in OpenMP, Proceedings of the First European Workshop on OpenMP, Lund, Sweden, 1999, pp 99–105. 

J. M. Bull and D. O’Neill, A microbenchmark suite for OpenMP 2.0,  SIGARCH Comput. Archit. News, vol. 29, no. 5, pp. 41–48, 2001. 

J. M. Bull, F. Reid and N. McDonnell, A microbenchmark suite for OpenMP tasks, in Proceedings of the 8th international conference on OpenMP in a Heterogeneous World (IWOMP '12) pp. 271-274, 2012.
