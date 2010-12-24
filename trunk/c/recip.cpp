#include <stdio.h>
#include "reciprocal.hpp"
#include <iostream>

int main()
{
	test t;
	t.t1(8);
	return 0;
}

int test::t1(int i)
{
	std::cout <<"introduction ..";
	printf ("%d\n",i);
	return 3*i;
}
