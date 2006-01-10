/*
*01-09-06
*	a test module for boost::dynamic_bitset and see whether it could hold 9 million edges' signature into memory
*	It turns out 9216883 edges, with 121-long sig vectors occupy 608M memory for 'unsigned int', 679M for 'unsigned long'
*
*
*/

#include <iostream>
#include <boost/dynamic_bitset.hpp>
#include <vector>
#include <boost/tokenizer.hpp>	//for tokenizer, parse input file
#include <fstream>
#include <boost/array.hpp>

int main(int argc, char* argv[]) {
	std::cerr<<"Read in graph from matrix_file "<<argv[1]<<"..."<<std::endl;
	std::ifstream datafile(argv[1]);
	std::vector<unsigned int > edge_tuple_vector;
	std::vector<boost::dynamic_bitset<> > bitset_vector;
	boost::array<unsigned int, 2> edge_tuple = {0,0};
	boost::dynamic_bitset<> sig_bitset;	//121 is a preset number
	sig_bitset.resize(121);
	int line_counter=0;
	boost::char_separator<char> sep(" \t");		//05-25-05	blank or '\t' is the separator
	typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
	for (std::string line; std::getline(datafile, line);) {
		tokenizer line_toks(line, sep);
		int i = 0;
		for (tokenizer::iterator tokenizer_iter = line_toks.begin(); tokenizer_iter!=line_toks.end();++tokenizer_iter)
		{
			if ((i == 0)  || (i==1))
				//edge_tuple[i] = atoi((*tokenizer_iter).c_str());
				edge_tuple_vector.push_back(atoi((*tokenizer_iter).c_str()));
			else
				sig_bitset[i-2] = atoi((*tokenizer_iter).c_str());
			i++;
		}
		//edge_tuple_vector.push_back(edge_tuple);
		bitset_vector.push_back(sig_bitset);
		line_counter ++;
		if (line_counter%5000==0)
			std::cerr<<"\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08"<<line_counter;
	}
	std::cerr<<"Done."<<std::endl;
	std::cout<<edge_tuple_vector[0]<<'\t'<<edge_tuple_vector[1]<<std::endl;
	for (boost::dynamic_bitset<>::size_type i = 0; i < bitset_vector[0].size(); ++i)
    	std::cout << bitset_vector[0][i];
	std::cout<<"Done."<<std::endl;
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
