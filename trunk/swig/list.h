#include <iostream>
#include <vector>
#include <hash_map.h>
using namespace std;

vector<float> python_call(vector<string> n_vector);

class List {
	public:
		List(char* m_name);
		~List();
		void print_name();
		vector<float> return_float_value();
		int  length;
		char* my_name;
		vector<float> value;

};
