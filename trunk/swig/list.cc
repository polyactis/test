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
