#include <iostream>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
using namespace std;

int main(void)
{
	//call a function
	double x = 5.0;
	double y = gsl_sf_bessel_J0(x);
	
	//output it
	cout<<"J0("<<x<<") = "<<y<<endl;
	//printf("J0(%g) = %.18e\n", x, y);
	
	//gsl constant
	cout<<M_EULER<<endl;

	//NAN
	double z = GSL_NAN;
	if(gsl_isnan(z))
	{
		cout <<z<<endl;
		cout <<"z is nan"<<endl;
	}

	//elementary function
	double log = gsl_log1p(0.0005);
	cout <<log<<endl;

	//inline function
	double max = GSL_MAX_DBL(y,log);
	cout<<max<<endl;

	//hypergeometric function
	double p_h = gsl_ran_hypergeometric_pdf(10,25,50,11);
	cout <<p_h<<endl;

	//chi-squared
	double q_c = gsl_cdf_chisq_Q(2, 10);
	cout <<q_c<<endl;
	return 0;
	
}
