/*
*Boost.Python's hello world example
*
*02-24-05 test dict, list, tuple python data structures.
*
*
*/
#include <iostream>
#include <boost/python.hpp>
#include <boost/graph/subgraph.hpp>	//for boost::subgraph

using namespace boost::python;
//using namespace boost;		//02-24-05 namespace conflict
char const* greet()
{
	return "hello, world";
}

class World
{
	public:
	World(std::string msg): msg(msg) {} // added constructor
	void set(std::string msg) { this->msg = msg; }
	std::string greet() { return msg; }
	boost::python::tuple return_keys(dict dic, int length);
	std::string msg;
};

boost::python::tuple World::return_keys(dict dic, int length)
{
	dict dc1;
	dict dc2;
	list k_list = dic.keys();
	for(int i=0; i<length; i++)
		std::cout<<extract<int>(k_list[i][0])<<"\t";
	std::cout<<std::endl;
	int len = extract<int>(k_list.attr("__len__")());
	std::cout<<"length of the dictionary is "<<len<<std::endl;
	for(int i=0; i<len;i++)
	{
		int g1 = extract<int>(k_list[i][0]);
		int g2 = extract<int>(k_list[i][1]);
		boost::python::tuple tup = boost::python::make_tuple(g1,g2);
		std::string s =extract<std::string>(dic[tup]);
		std::cout<<s<<std::endl;
	}
	dc1[make_tuple(1,2)]=1;
	dc2[make_tuple(2,3)]=2;
	list new_list;
	new_list.append(dc1);
	new_list.append(dc2);
	return make_tuple(new_list);
	
}


void f(str name)
{
    object n2 = name.attr("upper")();   // NAME = name.upper()
    str NAME = name.upper();            // better
    object msg = "%s is bigger than %s" % make_tuple(NAME,name);
}

BOOST_PYTHON_MODULE(hello)
{
	class_<World>("World", init<std::string>())
		.def("greet", &World::greet)
		.def("set", &World::set)
		.def("return_keys", &World::return_keys)
	;
}
