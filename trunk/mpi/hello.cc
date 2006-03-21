#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char *argv[])
{
	int rank, size;
	MPI::Init(argc,argv);
	rank = MPI::COMM_WORLD.Get_rank();
	size = MPI::COMM_WORLD.Get_size();
	cout << "Hello, world! I am " << rank << " Of " << size <<endl;

	MPI::Finalize();
	return 0;
}
