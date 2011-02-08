#include <omp.h>
#include <iostream>
#include <sstream>
int main(int argc, char *argv[]) {
	int th_id, nthreads;
	int maxNThreads;
	#ifdef _OPENMP
		std::cout << "Have OpenMP support\n";
	#else
		std::cout <<"no OpenMP support\n";
	#endif
#pragma omp parallel private(th_id)
	{
		th_id = omp_get_thread_num();
		std::ostringstream ss;
		ss << "Hello World from thread " << th_id << std::endl;
		std::cout << ss.str();
#pragma omp barrier
#pragma omp master
		{
			nthreads = omp_get_num_threads();
			maxNThreads = omp_get_max_threads();
			std::cout << "There are " << maxNThreads << " max no of threads. " << nthreads << " threads. " << " version: " << _OPENMP << std::endl;
		}
	}
	return 0;
}
