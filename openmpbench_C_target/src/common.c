// common.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include "common.h"
#include <sys/time.h>

// #define MAX_ARRAY_SIZE 16384
// double a[MAX_ARRAY_SIZE];  // 仅供 host 侧 init()/finalise() 使用

void init(int argc, char **argv) {
    // for (int i = 0; i < MAX_ARRAY_SIZE; ++i) a[i] = 0.0;
    printf("Initializing benchmark runtime environment...\n");

}

#pragma omp declare target
void delay_kernel(int delaylength, double *array)
{
    // Simple delay loop performing non-optimizable accumulation
    array[0]=1.0;
    for (int i = 0; i < delaylength; i++) {
        array[0] += i;
    }
    if (array[0] < 0)
	printf("%f \n", array[0]);
}
#pragma omp end declare target

void finalise(void) {
    printf("Finalizing benchmark.\n");
}
