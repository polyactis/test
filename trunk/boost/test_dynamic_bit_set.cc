#include <iostream>
#include <boost/dynamic_bitset.hpp>
#include <vector>
#include <boost/tokenizer.hpp>	//for tokenizer, parse input file
#include <fstream>
#include <boost/array.hpp>

#include <ext/hash_map>
#include <utility>
#include <boost/multi_array.hpp>
#define KEY(o1, o2) ((o1<<30) + o2)

typedef boost::multi_array<int, 2> edge_occurrence_matrix_type;
typedef edge_occurrence_matrix_type::index_range range;
typedef edge_occurrence_matrix_type::index index_type;

struct hash_edge_name
{
  size_t operator()(std::pair<long, long> edge_name) const
  {
    return ((edge_name.first<<30)+edge_name.second);
  }
};



int main(int argc, char* argv[]) {
	//01-23-06 testing hash_map, name space in __gnu_cxx
	/*
	__gnu_cxx::hash_map<std::pair <int, int>, int, hash_edge_name > edge_sig_vector_hash_map;
	std::pair<int, int> edge_name = std::make_pair(132, 432);
	edge_sig_vector_hash_map[edge_name] = 3;
	*/	
	
	std::cerr<<"Read in graph from matrix_file "<<argv[1]<<"..."<<std::endl;
	std::ifstream datafile(argv[1]);
	
	//01-23-06
	__gnu_cxx::hash_map<unsigned long, boost::dynamic_bitset<> > edge2bitset;

	
	std::vector<unsigned int > edge_tuple_vector;
	std::vector<boost::dynamic_bitset<> > bitset_vector;
	boost::array<unsigned long, 2> edge_tuple = {0,0};
	boost::dynamic_bitset<> sig_bitset;	//121 is a preset number
	int no_of_datasets = 121;
	sig_bitset.resize(no_of_datasets);
	int line_counter=0;
	boost::char_separator<char> sep(" \t");		//05-25-05	blank or '\t' is the separator
	typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
	for (std::string line; std::getline(datafile, line);) {
		tokenizer line_toks(line, sep);
		int i = 0;
		for (tokenizer::iterator tokenizer_iter = line_toks.begin(); tokenizer_iter!=line_toks.end();++tokenizer_iter)
		{
			if ((i == 0)  || (i==1))
				edge_tuple[i] = atol((*tokenizer_iter).c_str());
				//edge_tuple_vector.push_back(atoi((*tokenizer_iter).c_str()));
			else
				sig_bitset[i-2] = atoi((*tokenizer_iter).c_str());
			i++;
		}
		//edge_tuple_vector.push_back(edge_tuple);
		//01-23-06
		//bitset_vector.push_back(sig_bitset);
		edge2bitset[KEY(edge_tuple[0], edge_tuple[1])] = sig_bitset;
		line_counter ++;
		if (line_counter%5000==0)
			std::cerr<<"\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08"<<line_counter;
	}
	std::cerr<<"Done."<<std::endl;
	
	//01-23-06 recover the edge_name and sig_bitset
	__gnu_cxx::hash_map<unsigned long, boost::dynamic_bitset<> >::iterator edge2bitset_iter = edge2bitset.begin();
	/*
	unsigned long e_key = edge2bitset_iter->first;
	std::cout<<"key: "<<(e_key>>30)<<' '<<(edge2bitset_iter->first - ((e_key>>30)<<30)) <<" value: "<<edge2bitset_iter->second <<std::endl;
	*/
	std::cout<<"key: "<<edge2bitset_iter->first<<" value: "<<edge2bitset_iter->second <<std::endl;
	
	//01-23-06 construct a recurrence array for several edges
	int no_of_edges = 5;	//just 5 edges
	edge_occurrence_matrix_type edge_occurrence_matrix(boost::extents[no_of_edges][no_of_datasets]);
	//edge_occurrence_matrix_type::array_view<1>::type one_dim_view=edge_occurrence_matrix[boost::indices[0][range(0, no_of_datasets)] ];
	for(int i=0; i<no_of_edges; i++)
	{
		unsigned long e_key = edge2bitset_iter->first;
		std::cout<<"key: "<<(e_key>>30)<<' '<<(edge2bitset_iter->first - ((e_key>>30)<<30)) <<" value: "<<edge2bitset_iter->second <<std::endl;
		//one_dim_view = edge_occurrence_matrix[boost::indices[i][range(0, no_of_datasets)] ];
		sig_bitset = edge2bitset_iter->second;
		for (boost::dynamic_bitset<>::size_type j = 0; j < sig_bitset.size(); ++j)
    		edge_occurrence_matrix[i][j] = sig_bitset[j];
		edge2bitset_iter++;
	}
	std::cout<<"here's the combined recurrence_vector:"<<std::endl;
	//std::vector<float> recurrence_vector;
	for(index_type i=0; i<no_of_datasets; i++)
	{
		float recurrence =  0;
		for(index_type j=0; j<no_of_edges; j++)
			recurrence += edge_occurrence_matrix[j][i];
		recurrence /= no_of_edges;
		std::cout<<recurrence<<' ';
	}
	std::cout<<std::endl;
	
	/*01-23-06
	std::cout<<edge_tuple_vector[0]<<'\t'<<edge_tuple_vector[1]<<std::endl;
	for (boost::dynamic_bitset<>::size_type i = 0; i < bitset_vector[0].size(); ++i)
    	std::cout << bitset_vector[0][i];
	std::cout<<"Done."<<std::endl;
	*/
	//01-23-06 keep it infinitely running to see memory usage
	while (1)
		line_counter = 0;
	
	/*
  const boost::dynamic_bitset<> mask(160, 2730ul);
  std::cout << "mask = " << mask << std::endl;

  boost::dynamic_bitset<> x(160);

  std::cout << "Enter a 160-bit bitset in binary: " << std::flush;
  if (std::cin >> x) {
    std::cout << "input number:     " << x << std::endl;
    std::cout << "As unsigned long: " << x.to_ulong() << std::endl;
    std::cout << "And with mask:    " << (x & mask) << std::endl;
    std::cout << "Or with mask:     " << (x | mask) << std::endl;
    std::cout << "Shifted left:     " << (x << 1) << std::endl;
    std::cout << "Shifted right:    " << (x >> 1) << std::endl;
  }
  return EXIT_SUCCESS;
	*/
}
