#include "list.h"


List::List(char* m_name)
{
	my_name = m_name;
	cout<<my_name<<endl;
	cout<<"Here I start"<<endl;
}

List::~List()
{
	cout<<my_name<<endl;
	cout<<"finished"<<endl;
}

void List::print_name()
{
	cout<<my_name<<endl;
}

vector<float> List::return_float_value()
{
	value.push_back(1.0);
	value.push_back(2.0);
	return value;
}

vector<float> python_call(vector<string> n_vector)
{
	vector<string>::iterator v_iter;
	for(v_iter=n_vector.begin(); v_iter!=n_vector.end(); v_iter++)
		cout<<*v_iter<<endl;
	List instance("yuhuang");
	instance.return_float_value();
	return instance.value;
}
