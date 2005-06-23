#include <iostream>
#include <ostream>
#include <vector>
#include <ext/hash_map> 
#include <gsl/gsl_sf_bessel.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_cdf.h>
#include <queue>	//for priority_queue	06-22-05
#include <algorithm>	//for sort, for_each	06-22-05
#include "boost/tuple/tuple.hpp"	//for boost::tuple	06-22-05
using namespace std;
using namespace __gnu_cxx;

/*
 *
 * 02-15-05, #include<hash_map.h> gets backward warning, deprecated blahblah;
 * but #include<ext/hash_map> requires using namespace __gnu_cxx.
 * 
 */

typedef boost::tuple<std::string, std::string, float> edge_string_cor;

class cmp_edge	//06-22-05
{
public:
    bool operator() (const edge_string_cor & s1, const edge_string_cor & s2) const
    {
        return s1.get<2>() > s2.get<2>();	//compare the 2th element float value correlation
    }
};

//06-22-05	a binary predicate functor
struct small_edge : public binary_function<edge_string_cor, edge_string_cor, bool> {
	bool operator()(edge_string_cor x, edge_string_cor y) { return x.get<2>() < y.get<2>(); }
};

template<class T> struct print: public unary_function<T, void>
{
	print(ostream& out): os(out), count(0){}
	void operator()(T x){x = 1.0;os<<x<<' ';++count;}
	ostream& os;
	int count;
};

struct print_edge_string_cor: public unary_function<edge_string_cor, void>	//06-22-05	output an edge.
{
	print_edge_string_cor(ostream& out): os(out), count(0){}
	void operator()(edge_string_cor x){os<<x.get<0>()<<':'<<x.get<1>()<<"="<<x.get<2>()<<'\n';++count;}
	ostream& os;
	int count;
};

int main(void)
{
	//declare everything in a namespace
	//using namespace __gnu_cxx;
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
	hash_map<const char*, float>::iterator result = gene_label2index.find("YAR006W");
	float value = gene_label2index["YAR006X"];
	if(gene_label2index["YAR006W"])
		cout<<"YES"<<endl;
	else
		cout<<"NO"<<endl;
	if(value)
		cout <<"expression value of YAR006W is "<< gene_label2index["YAR006X"]<<endl;
	
	//06-22-05	test priority_queue
	
	priority_queue<edge_string_cor, vector<edge_string_cor>, small_edge > PQ;	//small_edge or cmp_edge are all ok. but not cmp_edge(), different from sort or other algorithm.
	PQ.push(boost::make_tuple("Mm.1","Mm.2",0.87));
	PQ.push(boost::make_tuple("Mm.2", "Mm.3", 0.57));
	PQ.push(boost::make_tuple("Mm.3", "Mm.5", 0.78));
	PQ.push(boost::make_tuple("Mm.5", "Mm.6", 0.57));
	edge_string_cor top_element = PQ.top();
	cout << "The top element of Q is "<<top_element.get<0>()<<":"<<top_element.get<1>()<<"="<<top_element.get<2>() << std::endl;
	PQ.pop();
	top_element = PQ.top();
	cout <<"After a pop, the top element of Q is "<<top_element.get<0>()<<":"<<top_element.get<1>()<<"="<<top_element.get<2>() << std::endl;
	PQ.pop();
	top_element = PQ.top();
	cout <<"pop again, then the top element of Q is "<<top_element.get<0>()<<":"<<top_element.get<1>()<<"="<<top_element.get<2>() << std::endl;
	
	
	//06-22-05	test the binary predicate, cmp_edge and the unary_function, print_edge_string_cor.
	vector<edge_string_cor> Q;
	Q.push_back(boost::make_tuple("Mm.1","Mm.2",0.87));
	Q.push_back(boost::make_tuple("Mm.2", "Mm.3", 0.57));
	Q.push_back(boost::make_tuple("Mm.3", "Mm.5", 0.78));
	Q.push_back(boost::make_tuple("Mm.5", "Mm.6", 0.57));
	sort (Q.begin(), Q.end(), cmp_edge());
	std::cout<<"edge_string_cor Vector  after sorted:"<<std::endl;
	std::for_each(Q.begin(), Q.end(), print_edge_string_cor(std::cout));
	
	return 0;
  
}
