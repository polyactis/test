#include <iostream>
#include <fstream>
#include <vector>
#include <bitset>
#include <cmath>
#define GENE_CUT_OFF 8
#define JK_CUT_OFF 7
#define COR_CUT_OFF 0.6
using namespace std;

typedef vector<float> vf;

//Usage:	'program_name' arg1 arg2 arg3
//			arg1 is the dataset source file
//			arg2 is the output file to hold the result
//			arg3 is the name of the dataset(whatever you like).
//			example: ./program_name dataset1 dataset1.gph dataset1

class graph_construct
{
	vector<vf> gene_array;
	vector<vf> cor_array;
	vector<bit_vector> mask_vector;
	vector<string> gene_labels_vector;
	char* graph_name;
	int no_of_genes;
	int no_of_cols;
	int no_of_valids;
	int no_of_cor6;
	int no_of_05;
	int no_of_025;
	int no_of_01;
	ifstream in;
	ofstream out;
	public:
		graph_construct(char* inf_name, char* outf_name, char* g_name);
		~graph_construct();
		void cor_array_readin(char* cor_fname);
		vector<string> general_split(string line, char ch);
		void input();
		void edge_construct();
		void output();
		float cor(vf v1, vf v2, int position);
		bit_vector bv_or(bit_vector bv1, bit_vector bv2);
		int bv_count(bit_vector bv);
		void split(string line);
};
