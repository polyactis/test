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
#include <vector>	//for vector

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
	boost::python::tuple return_keys(dict dic, int length, object data);
	object exercise(object ar);
	std::string msg;
};

boost::python::tuple World::return_keys(dict dic, int length, object data)
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
		//04-12-05	testing the conversion of data type between python and c++
		//'extract' works by some registered converters. i.e. python string to c++ string,
		//but not from python string to c++ int.
		if (s=="NA")
			std::cout<<"NA encounted"<<std::endl;
		if (s=="123")
		{
			int t = atoi(s.c_str());
			std::cout<<"integer encounted "<<t<<std::endl;
		}
		std::cout<<s<<std::endl;
	}
	dc1[make_tuple(1,2)]=1;
	dc2[make_tuple(2,3)]=2;
	list new_list;
	new_list.append(dc1);
	new_list.append(dc2);
	
	//04-15-05	testing the numeric object
	std::vector<float> data_vector;
	tuple shape = extract<tuple>(data.attr("shape"));
	int numRows = extract<int>(shape[0]);
	int numCols = extract<int>(shape[1]);
	std::cout<<"numRows: "<<numRows<<std::endl;
	std::cout<<"numCols: "<<numCols<<std::endl;
	
	
	return make_tuple(new_list);
	
}


//04-15-05	take a python Numeric or numarray /array as parameter, and return an array
object World::exercise(object ar)
{
	numeric::array br = extract<numeric::array>(ar);
	std::cout<<"elements of an array: "<<extract<int>(ar[0][0])<<std::endl;
	
	tuple shape = extract<tuple>(ar.attr("shape"));
	int numRows = extract<int>(shape[0]);
	int numCols = extract<int>(shape[1]);
	std::cout<<"numRows: "<<numRows<<std::endl;
	std::cout<<"numCols: "<<numCols<<std::endl;
	
	return numeric::array(
        make_tuple(
            make_tuple(1,2,3)
          , make_tuple(4,5,6)
          , make_tuple(7,8,9)
            )
        );
	
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
		.def("exercise", &World::exercise)
	;
	//04-15-05 function offered to select Numeric or numarray
	def("set_module_and_type", &numeric::array::set_module_and_type);
}
