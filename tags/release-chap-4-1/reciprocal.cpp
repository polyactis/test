#include <cassert>
#include "reciprocal.h"

double reciprocal (int i){
//i should be non-zero.
	assert (i!=0);
	return 1.0/i;
}
