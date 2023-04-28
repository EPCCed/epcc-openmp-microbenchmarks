
                                                                      
 #            OpenMP MicroBenchmark Suite - Version 4.0                     
                                                                           
produced by                                    
                                                                           
Mark Bull                   
                                                                          
at                                         
                                                                           
EPCC, University of Edinburgh                        
                                                                           
email: m.bull@epcc.ed.ac.uk            
                                                                           
                                                                           
This version copyright (c) The University of Edinburgh, 2023.        
                                                                           
                                                                           
Licensed under the Apache License, Version 2.0 (the "License"): you may not use this file except in compliance with the License.         
You may obtain a copy of the License at (http://www.apache.org/licenses/LICENSE-2.0)                           
                                                                           
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 





 Installation

 1. Clone the repository
 2. `cd openmpbench_C_v40`
 3. Edit the Makefile.defs as follows:
    * Set CC to the C compiler you wish to use (e.g. gcc pgcc icc xlc etc)
    * Set CFLAGS to any required C compiler flags to enable processing of 
      OpenMP directives (e.g. -fopenmp -mp, -omp); standard optimisation is 
      also recommended (e.g. -O).
    * Set LDFLAGS to any required C linker flags
    * Set CPPFLAGS to any required flags to 
      make the C compiler invoke cpp on .c and .h files
    * Set LIBS to any flags for linking with required libraries. 
    

3. Type "make" to build all 4 benchmarks or "make benchmark" where benchmark 
    is one of syncbench, taskbench, schedbench. By default "make" will build 
    arrybench executables with array sizes ranging in powers of 3 from 1 to 59049. To 
    build the array benchmark with an array size of arraysize, use 
    "make IDA=arraysize prog" where arraysize is a positive integer. 


Example Makefile.defs.* files are supplied for GNU, Cray, AMD and Intel compilers


# Running

1. Set OMP_NUM_THREADS to the number of OpenMP threads you want to run with, 
   e.g. export OMP_NUM_THREADS = 4
   

2. Run the benchmark with:
   ./\<benchmark\> 

   The output will go to STDOUT and thus you will probably want to re-direct 
   this to a file. ./<benchmark> -h will give the usage options.
	
   Available options are: 
	
	`--measureonly <selected measurement>`  (runs all by default) 
	
	`--outer-repetitions <outer-repetitions>` (default 20)
	
	`--test-time <target-test-time in microseconds>` (default 1000.00 microseconds)
	
	`--delay-time <delay-time in microseconds>` (default 0.1000 microseconds)
	
	`--delay-length <delay-length>` (default auto-generated based on processor speed)

=================
Additional notes
=================

 1. If you encounter problems with the value of innerreps becoming too 
    large (an error will be reported) try recompiling with a lower level of 
    optimisation, ideally with inlining turned off. 

 2. It is common to observe significant variability between the overhead 
    values obtained on different runs of the benchmark programs. Therefore, 
    it is advisable to run each benchmark, say, 10-20 times and average the 
    results obtained.

 3. You should use whatever mechanisms are at your disposal to ensure that 
    threads have exclusive or almost exclusive access to processors. You 
    should rejects runs where the standard deviation or number of outliers is 
    large: this is a good indication that the benchmark did not have almost 
    exclusive access to processors. 
