#include <iostream>
#include <ostream>
#include <vector>
#include <hash_map.h>
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
using namespace std;

template<class T> struct print: public unary_function<T, void>
{
	print(ostream& out): os(out), count(0){}
	void operator()(T x){x = 1.0;os<<x<<' ';++count;}
	ostream& os;
	int count;
};

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

	//vector, for_each and unary_function
	vector<float> vf;
	vf.resize(10);
	vf.push_back(GSL_NAN);
	cout<<"size of the vector:"<<vf.size()<<endl;
	for_each(vf.begin(),vf.end(),print<float>(cout));
	cout<<endl;
	vector<vector<float> > gene_array;
	gene_array.resize(100);
	if(gene_array[0].size()==0)
		cout<<"no values for gene:"<<0<<endl;
	
	//hash_map
	hash_map<const char*, float > gene_label2index;
	
	gene_label2index["YAR006W"] = 0.001;
	//hash_map<const char*, float>::iterator result = gene_label2index.find("YAR006W");
	float value = gene_label2index["YAR006X"];
	if(gene_label2index["YAR006W"])
		cout<<"YES"<<endl;
	else
		cout<<"NO"<<endl;
	if(value)
		cout <<"expression value of YAR006W is "<< gene_label2index["YAR006X"]<<endl;
	return 0;
	
}
