//:Fillvector.cpp
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <cmath>
#define CUT 0
using namespace std;

class graph
{
	int age;
public:
	graph(int s1);
		
};

graph::graph(int s1)
{
	age = s1;
}

int main(int argc, char* argv[]) {

	vector<string> v;
	ifstream in("Fillvector.cpp");
	string line;
	ofstream out(argv[1], ios::app | ios::out);

	string init="-0.6845";
	
	float x = atof(init.c_str());
	x /= 2.0;
	float y = NAN;
	char* name = argv[1];
	if (x>CUT)
		cout<<"y:\t"<<name<<endl;
	//ofstream out("tmp", ios::app | ios::out);
	//out.open("tmp", ios::app | ios::out);
	
	vector<float> gene_vector;
	typedef vector<float> vf;
	vector<vf> array_vector;
	string bitstr="00010011";
	bitset<8> bit_b(bitstr);
	bit_b[7]=1;
	bit_vector bv;
	bit_vector bv_a(8);
	bitset<8> bit_c(1);
	bit_vector::iterator it;
	for (int i=0; i<bit_b.size(); i++)
		bv.push_back(true);
	for (int i=0; i<bv.size(); i++)
		cout<<bv[i];
	//for (bit_vector::iterator it=bv.begin(); it<bv.end(); ++it)
	//	cout<<*it;
	cout<<endl;
	bitset<8> bit_d=bit_b|bit_c ;
	cout<<"bit_b\t"<<bit_b<<endl;
	cout<<"bit_c\t"<<bit_c<<endl;
	cout<<"bit_d\t"<<bit_d<<endl;

	cout <<"#bits set:\t"<<bit_d.count()<<endl; 
	
	while(getline(in,line))
		v.push_back(line);
	for (int i=v.size()-1;i>=0;i--)
		out << i<<": "<< v[i]<<endl;
}
