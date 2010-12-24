#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#define CHUNKSIZE 100 /*defines the chunk size as 1 contiguous iteration*/

int main(int argc, char *argv[]) {
	int th_id, nthreads;
#pragma omp parallel private(th_id)
	{
		th_id = omp_get_thread_num();
		printf("Hello World from thread %d\n", th_id);
#pragma omp barrier
		if (th_id == 0) {
			nthreads = omp_get_num_threads();
			printf("There are %d threads\n", nthreads);
		}
	}

	const int N = 100000000;
	int i, a[N];

#pragma omp parallel for
	for (i = 0; i < N; i++)
		a[i] = 2 * i;

	/*
	int i, j, k;
	int N = 100000000;
	int M = 1000;
	int a = 0;
#pragma omp parallel private(k)
	{
		//Starts the work sharing construct
#pragma omp for schedule(dynamic, CHUNKSIZE)
		for (i = 2; i <= N - 1; i++)
			//for (j = 2; j <= i; j++)
			//for (k = 1; k <= M; k++)
			a = 1;
		//b[i][j] += a[i - 1][j] / k + a[i + 1][j] / k;
	}
	*/
	return EXIT_SUCCESS;
}
