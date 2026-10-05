void init(int argc, char **argv);

#pragma omp declare target
void delay(int delaylength);
void delay_kernel(int delaylength, double a[1]);
#pragma omp end declare target

// Function declarations
void compute_offloading_time(double *intercept_avg, double *intercept_err,
                             double *min_avg, double *min_err,
                             int method_id, const char *method_name, int N);
void warmup_cache(int method, int N, int thread_count, int team_count);

void device_target(int offloading_method, int set, int run, double *a, int N, int thread_count, int team_count);
static void shuffle_indices_local(int *perm, int n, unsigned int seed);


void finalise(void);