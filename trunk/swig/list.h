#include <iostream>
using namespace std;

class List {
	public:
		List(char* m_name);
		~List();
		void print_name();
		int  length;
		char* my_name;

};
